from telebot.types import Message
from datetime import datetime

from database.msg_templates import REPLIES
from database.dbworker import get_fraction_usernames, get_usernames, get_pawns_usernames

from functions.decorators import group_required, admin_required, spam_checker
from functions.keyboards import create_group_markup

from loader import bot, engine

@bot.message_handler(commands=["light", "forest", "tech", "dark", "magic"])
@bot.message_handler(
    func=lambda message: 
        message.text == "Лесной союз 🍃" or
        message.text == "Магический совет 🔮" or
        message.text == "Королевство света ☀️" or
        message.text == "Техногенное общество 💡" or
        message.text == "Тёмные владения 🦇")
@spam_checker
@group_required
@admin_required
def fraction_command(message: Message) -> None:
    """This command will mention all registered users who choosed fractions for dragon

    Args:
        message (Message): Object, that contains information of received message
    """
    bot.reply_to(
        message, 
        REPLIES["before_mention"], 
        reply_markup=create_group_markup()
    )
    
    mention_message = ""
    usernames = get_fraction_usernames(message.text, engine)
    if usernames == []:
        bot.reply_to(message, REPLIES["no_fraction_users"])
        return

    for username in usernames:
        mention_message += f"@{username} "
    mention_message = str.rstrip(mention_message)
    match message.text:
        case fraction if fraction in ["Лесной союз 🍃", "/forest"]:
            mention_message += REPLIES["forest_mention"]
        case fraction if fraction in ["Магический совет 🔮", "/magic"]:
            mention_message += REPLIES["magic_mention"]
        case fraction if fraction in ["Королевство света ☀️", "/light"]:
            mention_message += REPLIES["light_mention"]
        case fraction if fraction in ["Техногенное общество 💡","/tech"]:
            mention_message += REPLIES["tech_mention"]
        case fraction if fraction in ["Тёмные владения 🦇", "/dark"]:
            mention_message += REPLIES["dark_mention"]

    bot.reply_to(message, mention_message)

    print("{date} {username} with id {id} called \"{fraction}\" in {chat_id}".format(date=datetime.now(), username=message.from_user.username, fraction=message.text, id=message.from_user.id, chat_id=message.chat.id))


@bot.message_handler(commands=["everyone"])
@bot.message_handler(func=lambda message: message.text == "@all 📢")
@spam_checker
@group_required
@admin_required
def everyone_command(message: Message) -> None:
    """This command will mention all registered users in database

    Args:
        message (Message): Object, that contains information of received message
    """
    bot.reply_to(
        message, 
        REPLIES["before_mention"], 
        reply_markup=create_group_markup()
    )

    mention_message = ""
    all_usernames = get_usernames(engine)
    for username in all_usernames:
        mention_message += f"@{username} "
    mention_message = str.rstrip(mention_message)
    mention_message += REPLIES["after_everyone"]
    bot.reply_to(message, mention_message)

    print("{date} {username} with id {id} called \"/everyone\" in {chat_id}".format(date=datetime.now(), username=message.from_user.username, id=message.from_user.id, chat_id=message.chat.id))


@bot.message_handler(commands=["banshee", "tesla", "robot", "panda"])
@bot.message_handler(
    func=lambda message: 
        message.text == "Банши 😈" or
        message.text == "Тесла ⚡️" or
        message.text == "Робот 🤖" or
        message.text == "Панда 🐼"
    )
@spam_checker
@group_required
@admin_required
def paws_command(message: Message) -> None:
    """This command will mention all registered users who choosed exact event pawns

    Args:
        message (Message): Object, that contains information of received message
    """
    bot.reply_to(
        message, 
        REPLIES["before_mention"], 
        reply_markup=create_group_markup()
    )
    
    mention_message = ""
    usernames = get_pawns_usernames(message.text, engine)
    if usernames == []:
        bot.reply_to(message, REPLIES["no_pawns_users"])
        return

    for username in usernames:
        mention_message += f"@{username} "
    mention_message = str.rstrip(mention_message)
    match message.text:
        case pawns if pawns in ["Банши 😈", "/banshee"]:
            mention_message += REPLIES["banshee_mention"]
        case pawns if pawns in ["Тесла ⚡️", "/tesla"]:
            mention_message += REPLIES["tesla_mention"]
        case pawns if pawns in ["Робот 🤖", "/robot"]:
            mention_message += REPLIES["robot_mention"]
        case pawns if pawns in ["Панда 🐼","/panda"]:
            mention_message += REPLIES["panda_mention"]

    bot.reply_to(message, mention_message)

    print("{date} {username} with id {id} called \"{pawns}\" in {chat_id}".format(date=datetime.now(), username=message.from_user.username, pawns=message.text, id=message.from_user.id, chat_id=message.chat.id))
