from telebot.types import Message

from database.msg_templates import REPLIES
from database.dbworker import add_templates

from loader import bot, engine

from functions.funcs import in_group, stop_talking, is_member, is_admin
from functions.keyboards import create_start_markup, create_stop_markup, create_unlogged_markup

ALPHABET = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"

@bot.message_handler(commands=["new"])
@bot.message_handler(func=lambda message: message.text == "Создать шаблон 📝")
def new_command(message: Message) -> None:
    """Handler that can help leader add his own templates

    Args:
        message (Message): Object, that contains information of received message
    """

    if in_group(message):
        return    

    if not is_member(message):
        bot.reply_to(message, REPLIES["not_logged"], reply_markup=create_unlogged_markup())
        return
    
    if not is_admin(message.from_user.id):
        bot.reply_to(message, REPLIES["rights_required"])
        return

    bot.reply_to(message, REPLIES["add_template"], reply_markup=create_stop_markup())
    bot.register_next_step_handler(message, add_template)

    print("{username} with id {id} called \"/new\" in {chat_id}".format(username=message.from_user.username, id=message.from_user.id, chat_id=message.chat.id))


def add_template(message: Message) -> None:
    """Function that add leader template

    Args:
        message (Message): Object, that contains information of received message
    """

    if stop_talking(message):
        return
    
    user_template = ""

    for word in str.split(message.text):
        if "имя_игрока" in word:
            user_template += "{rr_name}"
            if word[-1].lower() not in ALPHABET:
                user_template += word[-1]
        else:
            user_template += word
        user_template += " "
    
    user_template = str.rstrip(user_template)

    add_templates(user_template, engine)
    bot.reply_to(message, REPLIES["template_created"], reply_markup=create_start_markup(message.from_user.id))