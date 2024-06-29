from telebot.types import Message

from datetime import datetime

from database.msg_templates import REPLIES
from database.dbworker import get_usernames

from functions.decorators import group_required, admin_required, spam_checker
from functions.keyboards import create_group_markup

from loader import bot, engine


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