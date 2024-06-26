from telebot.types import Message

from database.msg_templates import REPLIES

from loader import bot

from functions.keyboards import create_help_markup
from functions.decorators import chat_required, group_required

@bot.message_handler(func=lambda _: True)
@chat_required
def incorrect_command(message: Message) -> None:
    """Handler that provides work with synonims of the word "Hello" 
    to greet the user and notify him that he is doing something wrong.

    Args:
        message (Message): Object, that contains information of received message
    """
    bot.reply_to(message, REPLIES["incorrect"], reply_markup=create_help_markup())