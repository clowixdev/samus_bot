from telebot.types import Message

from database.msg_templates import REPLIES
from database.dbworker import get_fraction_usernames

from functions.decorators import group_required, admin_required
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
@group_required
@admin_required
def fraction_command(message: Message) -> None:
    """This command will mention all registered users who choosed kingdom light

    Args:
        message (Message): Object, that contains information of received message
    """

    bot.reply_to(
        message, 
        REPLIES["before_mention"], 
        reply_markup=create_group_markup())
    
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

    print("{username} with id {id} called \"{fraction}\" in {chat_id}".format(username=message.from_user.username, fraction=message.text, id=message.from_user.id, chat_id=message.chat.id))