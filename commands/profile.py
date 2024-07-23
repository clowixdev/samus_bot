from telebot.types import Message
from datetime import datetime

from database.msg_templates import REPLIES
from database.dbworker import get_user, update_username

from loader import bot, engine

from functions.funcs import cut_username, gen_fractions, is_admin, gen_pawns
from functions.decorators import chat_required, member_required, spam_checker

@bot.message_handler(commands=["profile"])
@bot.message_handler(func=lambda message: message.text == "Профиль 🪪")
@spam_checker
@chat_required
@member_required
def profile_command(message: Message)-> None:
    """Handler that provides work for "profile" function that will show your info

    Args:
        message (Message): Object, that contains information of received message
    """
    username = cut_username(message.text)
    if username == None:
        username = message.from_user.username
    elif (username != None and username != message.from_user.username) and (not is_admin(message.from_user.id)):
        bot.reply_to(message, REPLIES["rights_required"])
        return
    
    if cut_username(message.text) == None:
        user = get_user(message.from_user.id, None, engine)
    else:
        user = get_user(None, username, engine)

    if user == None:
        bot.reply_to(message, REPLIES["no_user"].format(username=username))
        return
    
    if (user.id == message.from_user.id) and (user.username != message.from_user.username):
        update_username(message.from_user.id, message.from_user.username, engine)
        user = get_user(message.from_user.id, None, engine)

    bot.reply_to(message, REPLIES["profile"].format(
        username=user.username, 
        rr_name=user.rr_name,
        crit_dmg=user.crit_dmg,
        uid=user.uid,
        platform=user.platform, 
        fractions=gen_fractions(user),
        pawns=gen_pawns(user)
    ))

    print("{date} {username} with id {id} called \"/profile\" in {chat_id}".format(date=datetime.now(), username=message.from_user.username, id=message.from_user.id, chat_id=message.chat.id))