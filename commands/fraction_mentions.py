from telebot.types import Message

from database.msg_templates import REPLIES
from database.dbworker import get_fraction_usernames

from functions.funcs import in_group, is_admin

from loader import bot, engine


@bot.message_handler(commands=["light", "forest", "tech", "dark", "magic"])
def everyone_command(message: Message) -> None:
    """This command will mention all registered users who choosed kingdom light

    Args:
        message (Message): Object, that contains information of received message
    """

    if not is_admin(message.from_user.id):
        bot.reply_to(message, REPLIES["rights_required"])
        return

    if in_group(message):
        mention_message = ""
        usernames = get_fraction_usernames(message.text, engine)
        if usernames == []:
            bot.send_message(message.chat.id, REPLIES["no_fraction_users"])
            return

        for username in usernames:
            mention_message += f"@{username} "
        mention_message = str.rstrip(mention_message)
        match message.text:
            case "/forest":
                mention_message += REPLIES["forest_mention"]
            case "/magic":
                mention_message += REPLIES["magic_mention"]
            case "/light":
                mention_message += REPLIES["light_mention"]
            case "/tech":
                mention_message += REPLIES["tech_mention"]
            case "/dark":
                mention_message += REPLIES["dark_mention"]

        bot.send_message(message.chat.id, mention_message)
    else:
        bot.reply_to(message, REPLIES["only_for_chat"])

    print("{username} with id {id} called \"{fraction}\" in {chat_id}".format(username=message.from_user.username, fraction=message.text, id=message.from_user.id, chat_id=message.chat.id))