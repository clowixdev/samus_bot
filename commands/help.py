from telebot.types import Message

from database.msg_templates import REPLIES

from loader import bot

from functions.funcs import in_group, is_member, is_admin
from functions.keyboards import create_start_markup, create_unlogged_markup


@bot.message_handler(commands=["help"])
@bot.message_handler(func=lambda message: message.text == "Помощь 📃")
def help_command(message: Message) -> None:
    
    """Handler that will send to user list of command that he provides

    Args:
        message (Message): Object, that contains information of received message
    """

    if in_group(message):
        return

    if not is_member(message):
        bot.reply_to(message, REPLIES["not_logged"], reply_markup=create_unlogged_markup())
        return
    
    bot.reply_to(message, REPLIES["help"])
    if is_admin(message.from_user.id):
        bot.reply_to(message, REPLIES["commands-admin"], reply_markup=create_start_markup(message.from_user.id))
    else: 
        bot.reply_to(message, REPLIES["commands-user"], reply_markup=create_start_markup(message.from_user.id))

    print("{username} with id {id} called \"/help\" in {chat_id}".format(username=message.from_user.username, id=message.from_user.id, chat_id=message.chat.id))
    
