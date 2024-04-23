from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from database.msg_templates import REPLIES

from loader import bot, engine, DEVS, ADMINS

from functions.funcs import in_group, gen_templates, is_member, is_admin
from functions.keyboards import create_start_markup, create_unlogged_markup

@bot.message_handler(commands=["view"])
@bot.message_handler(func=lambda message: message.text == "Просмотреть шаблоны 👀")
def view_command(message: Message) -> None:
    """Handler that allows leaders to see all the existing templates

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
        templates, _ = gen_templates()
        bot.reply_to(message, REPLIES["show_templates"])
        bot.reply_to(message, templates, reply_markup=create_start_markup(message.from_user.id))
    except ValueError as e:
        bot.reply_to(message, REPLIES["empty_templates"], reply_markup=create_start_markup(message.from_user.id))

    print("{username} with id {id} called \"/all\" in {chat_id}".format(username=message.from_user.username, id=message.from_user.id, chat_id=message.chat.id))
