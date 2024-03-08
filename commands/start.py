from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from database.msg_templates import REPLIES
from database.dbworker import get_user, gen_users

from loader import bot, engine, dev_id, leader_id

DEVS = [dev_id]

@bot.message_handler(commands=['start'])
def start_command(message: Message)-> None:
    """Handler that provides work of "/start" command.

    Args:
        message (Message): Object, that contains information of received message
    """
    bot.reply_to(message, REPLIES['start'])
    print(message.from_user.id, message.from_user.username)

@bot.message_handler(func=lambda _: True)
def incorrect_command(message: Message)-> None:
    """Handler that provides work with synonims of the word "Hello" 
    to greet the user and notify him that he is doing something wrong.

    Args:
        message (Message): Object, that contains information of received message
    """
    bot.reply_to(message, REPLIES['incorrect'])