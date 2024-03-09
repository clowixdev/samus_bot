from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from database.msg_templates import REPLIES
from database.msg_templates import TEMPLATES
from database.dbworker import get_user, gen_users, add_rr_name

from loader import bot, engine, dev_id, leader_id, secret_word

# DEVS = [int(dev_id), int(leader_id)]
DEVS = [int(dev_id)]

def gen_templates() -> str:
    """Function that generates one entire message with templates

    Returns:
        str: Generated message
    """
    message = 'Ваши шаблоны:\n\n'
    for id, template in enumerate(TEMPLATES):
        formatted_template = ''
        for word in str.split(TEMPLATES[template]):
            if word == '{rr_name}':
                formatted_template += 'имя_соклановца'
            else:
                formatted_template += word
            formatted_template += ' '
        formatted_template = str.rstrip(formatted_template)
        message += f"{id+1}) {formatted_template}\n\n"

    return message

def stop_talking(message: Message) -> bool:
    """Function that provides exit from dialogue.

    Args:
        message (Message): Object, that contains information of received message

    Returns:
        bool: Returns true if message match "stop-word" else false
    """
    if message.text.lower() == 'стоп':
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.reply_to(message, REPLIES['stop'])
        return True
    return False

@bot.message_handler(commands=['start'])
def start_command(message: Message)-> None:
    """Handler that provides work of "/start" command.

    Args:
        message (Message): Object, that contains information of received message
    """
    bot.reply_to(message, REPLIES['start'])
    bot.reply_to(message, REPLIES['register'])
    bot.register_next_step_handler(message, register_user)

    print(message.from_user.id, message.from_user.username)


# @bot.message_handler(commands=['register'])
def register_user(message: Message) -> None:
    """Handler that will add users to database and also add their ingame nickname

    Args:
        message (Message): Object, that contains information of received message
    """

    if stop_talking(message):
        return

    rr_username = message.text
    bot.reply_to(message, REPLIES['authenticate'])
    bot.register_next_step_handler(message, auth_member, username=rr_username)


# @bot.message_handler(commands=['auth'])
def auth_member(message: Message, username: list) -> None:
    """Handler that will check if user is a member of clan

    Args:
        message (Message): Object, that contains information of received message
    """

    if stop_talking(message):
        return

    if message.text == secret_word:
        user = get_user(message.from_user.id, message.from_user.username, engine)
        if user:
            add_rr_name(message.from_user.id, message.from_user.username, username, engine)
            bot.reply_to(message, REPLIES['auth_passed'])
        else:
            print("Error occured while creating user")
    else:
        bot.reply_to(message, REPLIES['auth_failed'])
        print(f"auth failed by {message.from_user.username}")


@bot.message_handler(commands=['all'])
def mention_all(message: Message) -> None:
    """Handler that allows leaders to contact all clan members

    Args:
        message (Message): Object, that contains information of received message
    """

    if stop_talking(message):
        return

    if message.from_user.id in DEVS:
        bot.reply_to(message, REPLIES['choose_template'])
        bot.reply_to(message, gen_templates())
        bot.register_next_step_handler(message, choose_template)
    else:
        print("Permission error")


# @bot.message_handler(func=lambda _: False)
def choose_template(message: Message) -> None:
    """Handler that will send choosen template to all members of the clan

    Args:
        message (Message): Object, that contains information of received message
        template_id (int): ID of choosen template
    """

    if stop_talking(message):
        return

    for user in gen_users(engine):
        if user.id == message.from_user.id:
            bot.send_message(user.id, TEMPLATES[message.text].format(rr_name=user.rr_name))
            continue
        else:
            bot.send_message(user.id, TEMPLATES[message.text].format(rr_name=user.rr_name))


@bot.message_handler(commands=['new'])
def handle_new(message: Message) -> None:
    """Handler that can help leader add his own templates

    Args:
        message (Message): Object, that contains information of received message
    """
    bot.reply_to(message, REPLIES['add_template'])
    bot.register_next_step_handler(message, add_template)


def add_template(message: Message) -> None:
    """Function that add leader template

    Args:
        message (Message): Object, that contains information of received message
    """
    last_key = ''
    user_template = ''

    for keys in TEMPLATES:
        last_key = keys
    last_key = str(int(last_key)+1)

    for word in str.split(message.text):
        if 'имя_игрока' in word:
            user_template += "{rr_name}"+word[-1]
        else:
            user_template += word
        user_template += ' '
    
    user_template = str.rstrip(user_template)

    TEMPLATES[last_key] = user_template
    print(TEMPLATES)


@bot.message_handler(func=lambda _: True)
def incorrect_command(message: Message)-> None:
    """Handler that provides work with synonims of the word "Hello" 
    to greet the user and notify him that he is doing something wrong.

    Args:
        message (Message): Object, that contains information of received message
    """
    bot.reply_to(message, REPLIES['incorrect'])