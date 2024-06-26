from telebot.types import Message

from database.msg_templates import REPLIES
from database.dbworker import get_user, delete_user

from loader import bot, engine, CHATS

from functions.funcs import cut_username
from functions.decorators import group_required, admin_required

@bot.message_handler(commands=["kick"])
@group_required
@admin_required
def kick_command(message: Message)-> None:
    """Handler that provides work of "/kick" command. User will be kicked from all chats and removed from base

    Args:
        message (Message): Object, that contains information of received message
    """

    username = cut_username(message.text)
    user_to_kick = get_user(None, username, engine)

    if user_to_kick == None:
        bot.reply_to(message, REPLIES["kick_error_msg"])
    else:
        bot.reply_to(message, REPLIES["kick_msg"].format(username=user_to_kick.username, rr_name=user_to_kick.rr_name))

        for chat in CHATS:
            bot.kick_chat_member(chat, get_user(None, username, engine).id)
    
        delete_user(user_to_kick.id, engine)

    print("{username} with id {id} called \"/kick\" in {chat_id}".format(username=message.from_user.username, id=message.from_user.id, chat_id=message.chat.id))    