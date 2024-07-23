from telebot.types import Message
from datetime import datetime

from database.msg_templates import REPLIES
from database.dbworker import add_templates

from loader import bot, engine, ADMINS, DEVS, media_groups

from functions.funcs import stop_talking
from functions.keyboards import create_start_markup, create_stop_markup
from functions.decorators import chat_required, admin_required, member_required, spam_checker

ALPHABET = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"

@bot.message_handler(commands=["new"])
@bot.message_handler(func=lambda message: message.text == "Создать шаблон 📝")
@spam_checker
@chat_required
@member_required
@admin_required
def new_command(message: Message) -> None:
    """Handler that can help leader add his own templates

    Args:
        message (Message): Object, that contains information of received message
    """

    bot.reply_to(message, REPLIES["add_template"], reply_markup=create_stop_markup())
    media_groups[message.from_user.id] = []
    bot.register_next_step_handler(message, add_template)

    print("{date} {username} with id {id} called \"/new\" in {chat_id}".format(date=datetime.now(), username=message.from_user.username, id=message.from_user.id, chat_id=message.chat.id))    


def add_template(message: Message) -> None:
    """Function that forming template by gathering photos and captions

    Args:
        message (Message): Object, that contains information of received message
    """

    if stop_talking(message):
        return

    if message.photo is not None:
        photo_info = bot.get_file(message.photo[-1].file_id)
        photo_bytes = bot.download_file(photo_info.file_path)
        media_groups[message.from_user.id] += [photo_bytes]

    user_template = ""
    user_text = message.text or message.caption

    for word in str.split(user_text):
        if "имя_игрока" in word:
            user_template += "{rr_name}"
            if word[-1].lower() not in ALPHABET:
                user_template += word[-1]
        else:
            user_template += word
        user_template += " "
    
    user_template = str.rstrip(user_template)

    bot.register_next_step_handler(message, add_description, user_template)
    bot.reply_to(message, REPLIES["template_added"], reply_markup=create_stop_markup())


def add_description(message: Message, template: str) -> None:
    """Function that adds description to a tempate and adds it to a database

    Args:
        message (Message): Object, that contains information of received message
        media_group_id
    """

    if stop_talking(message):
        return
    
    if message.from_user.id is not None and len(media_groups[message.from_user.id]) > 5:
        del(media_groups[message.from_user.id])
        bot.reply_to(message, REPLIES["pictures_amt_error"], reply_markup=create_stop_markup())
        new_command(message)
        return

    add_templates(template, media_groups[message.from_user.id], message.text, engine)
    del(media_groups[message.from_user.id])
    bot.reply_to(message, REPLIES["template_created"], reply_markup=create_start_markup(message.from_user.id))