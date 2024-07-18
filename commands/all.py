from telebot.types import Message, InputMediaPhoto
from datetime import datetime

from database.msg_templates import REPLIES
from database.dbworker import gen_users

from loader import bot, engine

from functions.funcs import stop_talking, gen_templates, get_template
from functions.keyboards import create_all_markup, create_start_markup, create_stop_markup
from functions.decorators import chat_required, member_required, admin_required, spam_checker


@bot.message_handler(commands=["all"])
@bot.message_handler(func=lambda message: message.text == "Рассылка клану 📨")
@spam_checker
@chat_required
@member_required
@admin_required
def all_command(message: Message) -> None:
    """Handler that allows leaders to contact all clan members

    Args:
        message (Message): Object, that contains information of received message
    """

    try:
        templates, templates_amt = gen_templates()
        bot.reply_to(message, REPLIES["choose_template"])
        bot.reply_to(message, templates, reply_markup=create_all_markup(templates_amt))
        bot.register_next_step_handler(message, choose_template)
    except ValueError as e:
        bot.reply_to(message, REPLIES["empty_templates"], reply_markup=create_start_markup(message.from_user.id))

    print("{date} {username} with id {id} called \"/all\" in {chat_id}".format(date=datetime.now(), username=message.from_user.username, id=message.from_user.id, chat_id=message.chat.id))


def choose_template(message: Message) -> None:
    """Handler that will send choosen template to all members of the clan

    Args:
        message (Message): Object, that contains information of received message
        template_id (int): ID of choosen template
    """

    if stop_talking(message):
        return
    
    if message.text == "Отправить без сохранения 📋" or message.text == "0":
        bot.send_message(message.from_user.id, REPLIES["send_without_storing"], reply_markup=create_stop_markup())
        bot.register_next_step_handler(message, send_without_storing)
        return
    
    template = get_template(message, all_command)

    for user in gen_users(engine):
        if user.id == message.from_user.id:
            continue
        else:
            if (template.photo1 is None):
                bot.send_message(user.id, (template.template).format(rr_name=user.rr_name))
            else:
                media_group = [InputMediaPhoto(template.photo1, caption=template.template)]
                if template.photo2 is not None:
                    media_group += [InputMediaPhoto(template.photo2)]
                if template.photo3 is not None:
                    media_group += [InputMediaPhoto(template.photo3)]
                if template.photo4 is not None:
                    media_group += [InputMediaPhoto(template.photo4)]
                if template.photo5 is not None:
                    media_group += [InputMediaPhoto(template.photo5)]

                bot.send_media_group(user.id, media_group)
    bot.send_message(message.from_user.id, REPLIES["msg_sent"], reply_markup=create_start_markup(message.from_user.id))


def send_without_storing(message: Message) -> None:
    """This handler will allow leader to send message right now without saving it

    Args:
        message (Message): Object, that contains information of received message
    """

    if stop_talking(message):
        return
    
    message_text = message.text or message.caption
    
    for user in gen_users(engine):
        if user.id == message.from_user.id:
            continue
        else:
            bot.send_message(user.id, message_text)
    bot.send_message(message.from_user.id, REPLIES["msg_sent"], reply_markup=create_start_markup(message.from_user.id))