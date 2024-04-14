from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from database.msg_templates import REPLIES

from loader import bot, engine, DEVS

from functions.funcs import in_group, gen_templates
from functions.keyboards import create_start_markup

@bot.message_handler(commands=["view"])
@bot.message_handler(func=lambda message: message.text == "Просмотреть шаблоны 👀")
def view_templates(message: Message) -> None:
    """Handler that allows leaders to see all the existing templates

    Args:
        message (Message): Object, that contains information of received message
    """
    if in_group(message):
        return
    
    if message.from_user.id in DEVS:
        try:
            templates, _ = gen_templates()
            bot.reply_to(message, REPLIES["show_templates"])
            bot.reply_to(message, templates, reply_markup=create_start_markup())
        except ValueError as e:
            bot.reply_to(message, REPLIES["empty_templates"], reply_markup=create_start_markup())
    else:
        print("Permission error")

    print("{username} with id {id} called \"/all\" in {chat_id}".format(username=message.from_user.username, id=message.from_user.id, chat_id=message.chat.id))
