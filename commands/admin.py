from telebot.types import Message
from datetime import datetime

from database.dbworker import gen_users, delete_user, blacklist_user, whitelist_user

from loader import bot, engine, main_chat_id, ADMINS, DEVS, blacklist
from functions.decorators import dev_required, spam_checker
from functions.funcs import cut_username, cut_id


@bot.message_handler(commands=["clear"])
@spam_checker
@dev_required
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
def stats_command(message: Message)-> None:
    """Handler that will provide work for stats command that will give me brief info about clan

    Args:
        message (Message): Object, that contains information of received message
    """
    all_users = gen_users(engine)
    for id, user in enumerate(all_users, 1):
        msg = f"DEV: {id}) @{user.username} - {user.rr_name} - {user.crit_dmg}%"
        msg += " " * (60 - len(msg))
        if user.id in ADMINS:
            msg += " - ADMIN"
        if user.id in DEVS:
            msg += " - DEV"
        
        print(msg)

    print(f"DEV: total {len(all_users)} users registered and {bot.get_chat_member_count(main_chat_id) - 2} total")

    bot.reply_to(message, "Printed all the stats, check the console")
    print("{date} DEV: {username} with id {id} called \"/stats\" in {chat_id}".format(date=datetime.now(), username=message.from_user.username, id=message.from_user.id, chat_id=message.chat.id))


@bot.message_handler(commands=["blacklist", "whitelist"])
@spam_checker
@dev_required
def list_command(message: Message)-> None:
    """Handler that will provide work for blacklist/whitelist command 
    that will made bot to ignore/unignore user who is in blacklist

    Args:
        message (Message): Object, that contains information of received message. Contains id or username
    """
    id = ""

    username = cut_username(message.text)
    if username == None:
        id = cut_id(message.text)
    else:
        id = None

    if id == None and username == None:
        bot.reply_to(message, "Printed a blacklist, check the console")
        print(f"{datetime.now()} DEV: current blacklist: {blacklist}")

    if "/blacklist" in message.text and (username != None or id != None):
        blacklist_user(username if username is not None else id, blacklist)
        bot.reply_to(message, f"Successfully blacklisted an entity: {username if username is not None else id}")
        print("{date} DEV: {username} with id {id} blacklisted {user}".format(
            date=datetime.now(), 
            username=message.from_user.username, 
            id=message.from_user.id, 
            user=(username if username != None else id))
            )
    
    elif "/whitelist" in message.text and (username != None or id != None):
        if not whitelist_user(username if username != None else id, blacklist):
            bot.reply_to(message, "Something went wrong, check the console")
            print(f"{' ' * 32} No such entity in blacklist: {username if username != None else id}")
        else:
            print("{date} DEV: {username} with id {id} whitelisted {user}".format(
            date=datetime.now(), 
            username=message.from_user.username, 
            id=message.from_user.id, 
            user=(username if username != None else id))
            )