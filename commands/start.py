from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from database.msg_templates import REPLIES
from database.dbworker import get_user, gen_users, add_rr_name

from loader import bot, engine, dev_id, leader_id, secret_word

DEVS = [dev_id, leader_id]

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

@bot.message_handler(commands=['register'])
def register_user(message: Message) -> None:
    """Handler that will add users to database and also add their ingame nickname

    Args:
        message (Message): Object, that contains information of received message
    """
    rr_username = message.text
    bot.reply_to(message, REPLIES['authenticate'])
    bot.register_next_step_handler(message, auth_member, username=rr_username)

@bot.message_handler(commands=['auth'])
def auth_member(message: Message, username: list) -> None:
    """Handler that will check if user is a member of clan

    Args:
        message (Message): Object, that contains information of received message
    """
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


@bot.message_handler(func=lambda _: True)
def incorrect_command(message: Message)-> None:
    """Handler that provides work with synonims of the word "Hello" 
    to greet the user and notify him that he is doing something wrong.

    Args:
        message (Message): Object, that contains information of received message
    """
    bot.reply_to(message, REPLIES['incorrect'])