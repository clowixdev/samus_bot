from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, PollAnswer

from database.msg_templates import REPLIES
from database.dbworker import get_user

from loader import bot, DEVS, ADMINS, engine

from functions.funcs import in_group, cut_username, gen_fractions, is_member, is_admin
from functions.keyboards import create_start_markup, create_unlogged_markup

@bot.message_handler(commands=["profile"])
@bot.message_handler(func=lambda message: message.text == "Профиль 🪪")
def profile_command(message: Message)-> None:
    """Handler that provides work for "profile" function that will show your info

    Args:
        message (Message): Object, that contains information of received message
    """

    if not is_member(message):
        bot.reply_to(message, REPLIES["not_logged"], reply_markup=create_unlogged_markup())
        return
    
    username = cut_username(message.text)
    if username == None:
        username = message.from_user.username
    elif (username != None and username != message.from_user.username) and (not is_admin(message.from_user.id)):
        bot.reply_to(message, REPLIES["rights_required"])
        return

    user = get_user(None, username, engine)
    bot.reply_to(message, REPLIES["profile"].format(
        username=user.username, 
        rr_name=user.rr_name,
        crit_dmg=user.crit_dmg, 
        uid=user.uid,
        platform=user.platform, 
        fractions=gen_fractions(user)
    ), reply_markup=create_start_markup(message.from_user.id))

    print("{username} with id {id} called \"/profile\" in {chat_id}".format(username=message.from_user.username, id=message.from_user.id, chat_id=message.chat.id))