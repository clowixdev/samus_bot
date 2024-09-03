from telebot.types import Message
from datetime import datetime

from database.msg_templates import REPLIES

from loader import bot


@bot.message_handler(content_types=["new_chat_members"])
def welcome_message(message: Message) -> None:
    """Handler that will force bot to send welcome message to new user of a chat

    Args:
        message (Message): Object, that contains information of received message
    """
    bot.reply_to(message, REPLIES["welcome_message"])
    print("{date} {username} with id {id} entered our group chat in {chat_id}".format(date=datetime.now(), username=message.from_user.username, id=message.from_user.id, chat_id=message.chat.id))


@bot.message_handler(content_types=["left_chat_members"])
def leaving_message(message: Message) -> None:
    """Handler that will force bot to send leaving message to new user of a chat

    Args:
        message (Message): Object, that contains information of received message
    """
    bot.reply_to(message, REPLIES["leave_message"])
    print("{date} {username} with id {id} left our group chat in {chat_id}".format(date=datetime.now(), username=message.from_user.username, id=message.from_user.id, chat_id=message.chat.id))