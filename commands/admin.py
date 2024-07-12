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
    deleted_users = 0
    for user in all_users:
        if user.username == None:
            deleted_users += 1
            print(f"DEV: deleted user {user.rr_name} - {user.crit_dmg}%")
            delete_user(user.id, engine)

    bot.reply_to(message, f"Deleted {deleted_users} users, check the console")

    print("{date} DEV: {username} with id {id} called \"/clear\" in {chat_id}".format(date=datetime.now(), username=message.from_user.username, id=message.from_user.id, chat_id=message.chat.id))


@bot.message_handler(commands=["stats"])
@spam_checker
@dev_required
@chat_required
def stats_command(message: Message)-> None:
    """Handler that will provide work for stats command that will give me brief info about clan

    Args:
        message (Message): Object, that contains information of received message
    """

    all_users = gen_users(engine)
    for id, user in enumerate(user, 1):
        print(f"DEV: {id}) {user.username} - {user.rr_name} - {user.crit_dmg}%")

    print(f"DEV: total {len(all_users)} users registered")

    bot.reply_to(message, f"Printed all the stats, check the console")
    print("{date} DEV: {username} with id {id} called \"/stats\" in {chat_id}".format(date=datetime.now(), username=message.from_user.username, id=message.from_user.id, chat_id=message.chat.id))