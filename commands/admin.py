from telebot.types import Message
from datetime import datetime

from database.msg_templates import REPLIES
from database.dbworker import gen_users, delete_user

from loader import bot, engine
from functions.decorators import chat_required, dev_required, spam_checker


@bot.message_handler(commands=["clear"])
@spam_checker
@dev_required
@chat_required
def clear_command(message: Message)-> None:
    """Handler that provides work for "clear" function that will clear database from None username profiles

    Args:
        message (Message): Object, that contains information of received message
    """
    all_users = gen_users(engine)
    for user in all_users:
        if user.username == None:
            print(f"DEV: deleted user {user.rr_name} - {user.crit_dmg}%")
            delete_user(user.id, engine)

    print("{date} DEV: {username} with id {id} called \"/clear\" in {chat_id}".format(date=datetime.now(), username=message.from_user.username, id=message.from_user.id, chat_id=message.chat.id))