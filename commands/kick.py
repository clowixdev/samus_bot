from telebot.types import Message
from datetime import datetime

from database.msg_templates import REPLIES
from database.dbworker import get_user, delete_user

from loader import bot, engine

from functions.funcs import cut_username
from functions.decorators import group_required, admin_required, spam_checker

@bot.message_handler(commands=["kick"])
@spam_checker
@group_required
@admin_required
def kick_command(message: Message)-> None:
    """Handler that provides work of "/kick" command. User will be kicked removed from database

    Args:
        message (Message): Object, that contains information of received message
    """
    username = cut_username(message.text)
    user_to_kick = get_user(None, username, engine)

    if user_to_kick == None:
        bot.reply_to(message, REPLIES["kick_error_msg"])
    else:
        bot.reply_to(message, REPLIES["kick_msg"].format(username=user_to_kick.username, rr_name=user_to_kick.rr_name))
    
        delete_user(user_to_kick.id, engine)

    print("{date} {username} with id {id} called \"/kick\" in {chat_id}".format(date=datetime.now(), username=message.from_user.username, id=message.from_user.id, chat_id=message.chat.id))    