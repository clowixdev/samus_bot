from telebot.types import Message

from database.msg_templates import REPLIES
from database.dbworker import get_user, gen_users, add_rr_name, update_templates, get_templates, delete_template, get_usernames

from loader import bot, engine, secret_word, DEVS, ADMINS

from functions.funcs import in_group, stop_talking, gen_templates

ALPHABET = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

@bot.message_handler(commands=['new'])
def handle_new(message: Message) -> None:
    """Handler that can help leader add his own templates

    Args:
        message (Message): Object, that contains information of received message
    """

    if in_group(message):
        return

    bot.reply_to(message, REPLIES['add_template'])
    bot.register_next_step_handler(message, add_template)

    print("{username} with id {id} called '/new' in {chat_id}".format(username=message.from_user.username, id=message.from_user.id, chat_id=message.chat.id))


def add_template(message: Message) -> None:
    """Function that add leader template

    Args:
        message (Message): Object, that contains information of received message
    """

    if stop_talking(message):
        return
    
    user_template = ''

    for word in str.split(message.text):
        if 'имя_игрока' in word:
            user_template += "{rr_name}"
            if word[-1].lower() not in ALPHABET:
                user_template += word[-1]
        else:
            user_template += word
        user_template += ' '
    
    user_template = str.rstrip(user_template)

    last_key = ''
    new_template_id = 0
    templates = get_templates(engine)
    try:
        for key in templates:
            last_key = key
        new_template_id = str(last_key + 1)
    except Exception as e:
        print(e)

    update_templates(user_template, new_template_id, engine)
    bot.reply_to(message, REPLIES['template_created'])