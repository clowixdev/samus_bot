from telebot.types import Message

from database.msg_templates import REPLIES
from database.dbworker import get_user

from loader import bot, engine

from functions.funcs import cut_username, gen_fractions, is_member, is_admin, in_group
from functions.keyboards import create_unlogged_markup

@bot.message_handler(commands=["profile"])
@bot.message_handler(func=lambda message: message.text == "Профиль 🪪")
def profile_command(message: Message)-> None:
    """Handler that provides work for "profile" function that will show your info

    Args:
        message (Message): Object, that contains information of received message
    """

    if not is_member(message) and not in_group(message):
        bot.reply_to(message, REPLIES["not_logged"], reply_markup=create_unlogged_markup())
        return
    
    if not is_admin(message.from_user.id) and in_group(message):
        return
    
    username = cut_username(message.text)
    if username == None:
        username = message.from_user.username
    elif (username != None and username != message.from_user.username) and (not is_admin(message.from_user.id)):
        bot.reply_to(message, REPLIES["rights_required"])
        return

    user = get_user(None, username, engine)
    if user == None:
        bot.reply_to(message, REPLIES["no_user"].format(username=username))
        return
    
    bot.reply_to(message, REPLIES["profile"].format(
        username=user.username, 
        rr_name=user.rr_name,
        crit_dmg=user.crit_dmg, 
        uid=user.uid,
        platform=user.platform, 
        fractions=gen_fractions(user)
    ))

    print("{username} with id {id} called \"/profile\" in {chat_id}".format(username=message.from_user.username, id=message.from_user.id, chat_id=message.chat.id))