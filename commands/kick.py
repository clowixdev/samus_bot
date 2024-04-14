from telebot.types import Message

from database.msg_templates import REPLIES
from database.dbworker import get_user, delete_user

from loader import bot, engine, CHATS, ADMINS, DEVS

from functions.funcs import in_group, cut_username

@bot.message_handler(commands=["kick"])
def kick_command(message: Message)-> None:
    """Handler that provides work of "/kick" command. User will be kicked from all chats and removed from base

    Args:
        message (Message): Object, that contains information of received message
    """

    if not in_group(message):
        bot.reply_to(message, REPLIES["only_for_chat"])
        return
    
    if not (message.from_user.id in DEVS or message.from_user.id in ADMINS):
        bot.reply_to(message, REPLIES["rights_required"])
        return

    username = cut_username(message.text)
    user_to_kick = get_user(None, username, engine)

    if user_to_kick == None:
        bot.reply_to(message, REPLIES["kick_error_msg"])
    else:
        bot.reply_to(message, REPLIES["kick_msg"].format(username=user_to_kick.username, rr_name=user_to_kick.rr_name))

        for chat in CHATS:
            bot.kick_chat_member(chat, get_user(None, username, engine).id)
    
        delete_user(user_to_kick.id, engine)