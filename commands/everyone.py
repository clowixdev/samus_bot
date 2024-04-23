from telebot.types import Message

from database.msg_templates import REPLIES
from database.dbworker import get_usernames

from functions.funcs import is_member, in_group, is_admin
from functions.keyboards import create_unlogged_markup

from loader import bot, engine, DEVS, ADMINS


@bot.message_handler(commands=["everyone"])
def everyone_command(message: Message) -> None:
    """This command will mention all registered users in database

    Args:
        message (Message): Object, that contains information of received message
    """

    if not is_admin(message.from_user.id):
        bot.reply_to(message, REPLIES["rights_required"])
        return

    if in_group(message):
        mention_message = ""
        all_usernames = get_usernames(engine)
        for username in all_usernames:
            mention_message += f"@{username} "
        mention_message = str.rstrip(mention_message)
        mention_message += REPLIES["after_everyone"]
        bot.send_message(message.chat.id, mention_message)
    else:
        bot.reply_to(message, REPLIES["only_for_chat"])

    print("{username} with id {id} called \"/everyone\" in {chat_id}".format(username=message.from_user.username, id=message.from_user.id, chat_id=message.chat.id))