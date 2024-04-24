from telebot.types import Message

from database.msg_templates import REPLIES
from database.dbworker import gen_users, get_templates

from loader import bot, engine

from functions.funcs import in_group, stop_talking, gen_templates, is_member, is_admin
from functions.keyboards import create_all_markup, create_start_markup, create_stop_markup, create_unlogged_markup


@bot.message_handler(commands=["all"])
@bot.message_handler(func=lambda message: message.text == "Рассылка клану 📨")
def all_command(message: Message) -> None:
    """Handler that allows leaders to contact all clan members

    Args:
        message (Message): Object, that contains information of received message
    """

    if in_group(message):
        return

    if not is_member(message):
        bot.reply_to(message, REPLIES["not_logged"], reply_markup=create_unlogged_markup())
        return
    
    if not is_admin(message.from_user.id):
        bot.reply_to(message, REPLIES["rights_required"])
        return

    try:
        templates, templates_amt = gen_templates()
        bot.reply_to(message, REPLIES["choose_template"])
        bot.reply_to(message, templates, reply_markup=create_all_markup(templates_amt))
        bot.register_next_step_handler(message, choose_template)
    except ValueError as e:
        bot.reply_to(message, REPLIES["empty_templates"], reply_markup=create_start_markup(message.from_user.id))

    print("{username} with id {id} called \"/all\" in {chat_id}".format(username=message.from_user.username, id=message.from_user.id, chat_id=message.chat.id))


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
    
    templates = get_templates(engine)
    try:
        if len(message.text) == 1:
            template_id = int(message.text) - 1
        else:
            template_id = int(message.text[-3]) - 1
    except ValueError as e:
        bot.reply_to(message, REPLIES["invalid_key"])
        all_command(message)
        return

    for user in gen_users(engine):
        if user.id == message.from_user.id:
            continue
        else:
            try:
                bot.send_message(user.id, templates[template_id].format(rr_name=user.rr_name))
            except KeyError as e:
                bot.reply_to(message, REPLIES["invalid_key"])
                all_command(message)
                return
    bot.send_message(message.from_user.id, REPLIES["msg_sent"], reply_markup=create_start_markup(message.from_user.id))


def send_without_storing(message: Message) -> None:
    """This handler will allow leader to send message right now without saving it

    Args:
        message (Message): Object, that contains information of received message
    """

    if stop_talking(message):
        return

    for user in gen_users(engine):
        if user.id == message.from_user.id:
            continue
        else:
            bot.send_message(user.id, message.text)
    bot.send_message(message.from_user.id, REPLIES["msg_sent"], reply_markup=create_start_markup(message.from_user.id))