from telebot.types import Message
from datetime import datetime

from database.msg_templates import REPLIES

from loader import bot

from functions.funcs import is_admin
from functions.keyboards import create_start_markup, create_group_markup
from functions.decorators import member_required, spam_checker


@bot.message_handler(commands=["help"])
@bot.message_handler(func=lambda message: message.text == "Помощь 📃")
@spam_checker
@member_required
def help_command(message: Message) -> None:
    
    """Handler that will send to user list of command that he provides

    Args:
        message (Message): Object, that contains information of received message
    """        

    bot.reply_to(message, REPLIES["help"])
    if is_admin(message.from_user.id):
        if message.from_user.id != message.chat.id:
            bot.reply_to(message, REPLIES["commands_admin_group"], reply_markup=create_group_markup())
        else:
            bot.reply_to(message, REPLIES["commands_admin_chat"], reply_markup=create_start_markup(message.from_user.id))
    else:
        if message.from_user.id != message.chat.id:
            bot.reply_to(message, REPLIES["commands_user_group"])
        else:
            bot.reply_to(message, REPLIES["commands_user_chat"], reply_markup=create_start_markup(message.from_user.id))

    print("{date} {username} with id {id} called \"/help\" in {chat_id}".format(date=datetime.now(), username=message.from_user.username, id=message.from_user.id, chat_id=message.chat.id))