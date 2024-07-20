from telebot.types import Message, InputMediaPhoto
from datetime import datetime

from database.msg_templates import REPLIES
from database.dbworker import get_user

from loader import bot, engine

from functions.funcs import gen_templates, stop_talking, get_template
from functions.keyboards import create_start_markup, create_view_markup
from functions.decorators import chat_required, member_required, admin_required, spam_checker


@bot.message_handler(commands=["view"])
@bot.message_handler(func=lambda message: message.text == "Просмотреть шаблоны 👀")
@spam_checker
@chat_required
@member_required
@admin_required
def view_command(message: Message) -> None:
    """Handler that allows leaders to see all the existing templates

    Args:
        message (Message): Object, that contains information of received message
    """

    try:
        user = get_user(message.from_user.id, None, engine)
        templates, templates_amt = gen_templates(user.rr_name)
        bot.reply_to(message, REPLIES["show_templates"])
        bot.reply_to(message, templates, reply_markup=create_view_markup(templates_amt))
        bot.register_next_step_handler(message, view_template)
    except ValueError as e:
        bot.reply_to(message, REPLIES["empty_templates"], reply_markup=create_start_markup(message.from_user.id))

    print("{date} {username} with id {id} called \"/view\" in {chat_id}".format(date=datetime.now(), username=message.from_user.username, id=message.from_user.id, chat_id=message.chat.id))


def view_template(message: Message) -> None:
    """Function, that allows leader to check the template, not it's description

    Args:
        message (Message): Object, that contains information of received message
    """

    if stop_talking(message):
        return
    
    template = get_template(message, view_command)
    
    if template is not None:
        if (template.photo1 is None):
            bot.send_message(message.from_user.id, (template.template).format(rr_name="имя_соклановца"))
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

            bot.send_media_group(message.from_user.id, media_group)

        bot.send_message(message.from_user.id, REPLIES["msg_view"], reply_markup=create_start_markup(message.from_user.id))