from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, PollAnswer

from database.msg_templates import REPLIES
from database.dbworker import get_user

from loader import bot, DEVS, ADMINS, engine

from functions.funcs import in_group, cut_username, gen_fractions
from functions.keyboards import create_start_markup

@bot.message_handler(commands=["profile"])
@bot.message_handler(func=lambda message: message.text == "Профиль 🪪")
def profile_command(message: Message)-> None:
    """Handler that provides work for "profile" function that will show your info

    Args:
        message (Message): Object, that contains information of received message
    """
    
    if not (message.from_user.id in DEVS or message.from_user.id in ADMINS):
        bot.reply_to(message, REPLIES["rights_required"])
        return
    
    username = cut_username(message.text)
    if username == None:
        username = message.from_user.username
    user = get_user(None, username, engine)
    bot.reply_to(message, REPLIES["profile"].format(
        username=user.username, 
        rr_name=user.rr_name,
        crit_dmg=user.crit_dmg, 
        uid=user.uid,
        platform=user.platform, 
        fractions=gen_fractions(user)
    ), reply_markup=create_start_markup())
