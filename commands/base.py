from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton

from database.msg_templates import REPLIES
from database.dbworker import get_user, add_user

from loader import bot, engine, secret_word

from functions.funcs import in_group, stop_talking, is_member
from functions.keyboards import create_start_markup, create_help_markup, create_stop_markup, create_unlogged_markup


@bot.message_handler(commands=["start"])
@bot.message_handler(func=lambda message: message.text == "Начать ⭐")
def start_command(message: Message)-> None:
    """Handler that provides work of "/start" command.

    Args:
        message (Message): Object, that contains information of received message
    """

    if in_group(message):
        return
    
    bot.reply_to(message, REPLIES["start"])
    curr_user = get_user(message.from_user.id, message.from_user.username, engine)
    if curr_user == None:
        bot.reply_to(message, REPLIES["authenticate"], reply_markup=create_stop_markup())
        bot.register_next_step_handler(message, auth_member)
    else:
        bot.reply_to(message, REPLIES["logged"].format(rr_name=curr_user.rr_name), reply_markup=create_start_markup())

    print("{username} with id {id} called \"/start\" in {chat_id}".format(username=message.from_user.username, id=message.from_user.id, chat_id=message.chat.id))


def auth_member(message: Message) -> None:
    """Handler that will check if user is a member of clan

    Args:
        message (Message): Object, that contains information of received message
    """

    if stop_talking(message):
        return

    if message.text == secret_word:
        bot.reply_to(message, REPLIES["register"])
        bot.register_next_step_handler(message, register_user)
    else:
        bot.reply_to(message, REPLIES["auth_failed"])
        print(f"auth failed by {message.from_user.username}")
        bot.register_next_step_handler(message, auth_member)


def register_user(message: Message) -> None:
    """Handler that will add users to database and also add their ingame nickname

    Args:
        message (Message): Object, that contains information of received message
    """

    if stop_talking(message):
        return
    
    add_user(message.from_user.id, message.from_user.username, message.text, engine)
    bot.reply_to(message, REPLIES["auth_passed"], reply_markup=create_start_markup())


@bot.message_handler(commands=["help"])
@bot.message_handler(func=lambda message: message.text == "Помощь 📃")
def help_command(message: Message) -> None:
    """Handler that will send to user list of command that he provides

    Args:
        message (Message): Object, that contains information of received message
    """

    if not is_member(message):
        bot.reply_to(message, REPLIES["not_logged"], reply_markup=create_unlogged_markup())
        return
    
    bot.reply_to(message, REPLIES["help"])
    bot.reply_to(message, REPLIES["commands"], reply_markup=create_start_markup())


@bot.message_handler(func=lambda _: True)
def incorrect_command(message: Message) -> None:
    """Handler that provides work with synonims of the word "Hello" 
    to greet the user and notify him that he is doing something wrong.

    Args:
        message (Message): Object, that contains information of received message
    """
    if message.chat.id == message.from_user.id:
        bot.reply_to(message, REPLIES["incorrect"], reply_markup=create_help_markup())