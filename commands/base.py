from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton

from database.msg_templates import REPLIES
from database.dbworker import get_user, add_rr_name

from loader import bot, engine, secret_word

from functions.funcs import in_group, stop_talking
from functions.keyboards import create_start_markup, create_help_markup


@bot.message_handler(commands=["start"])
def start_command(message: Message)-> None:
    """Handler that provides work of "/start" command.

    Args:
        message (Message): Object, that contains information of received message
    """

    if in_group(message):
        return
    
    bot.reply_to(message, REPLIES["start"])
    curr_user_rr_name = get_user(message.from_user.id, message.from_user.username, engine)
    if curr_user_rr_name == "_empty_name_":
        bot.reply_to(message, REPLIES["register"])
        bot.register_next_step_handler(message, register_user)
    else:
        bot.reply_to(message, REPLIES["logged"].format(rr_name=curr_user_rr_name), reply_markup=create_start_markup())

    print("{username} with id {id} called \"/start\" in {chat_id}".format(username=message.from_user.username, id=message.from_user.id, chat_id=message.chat.id))


def register_user(message: Message) -> None:
    """Handler that will add users to database and also add their ingame nickname

    Args:
        message (Message): Object, that contains information of received message
    """

    if stop_talking(message):
        return

    bot.reply_to(message, REPLIES["authenticate"])
    bot.register_next_step_handler(message, auth_member, username=message.text)


def auth_member(message: Message, username: str) -> None:
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
            bot.reply_to(message, REPLIES["auth_passed"])
        else:
            print("Error occured while getting user from db")
    else:
        bot.reply_to(message, REPLIES["auth_failed"])
        print(f"auth failed by {message.from_user.username}")


@bot.message_handler(commands=["help"])
@bot.message_handler(func=lambda message: message.text == "Помощь 📃")
def help_command(message: Message) -> None:
    """Handler that will send to user list of command that he provides

    Args:
        message (Message): Object, that contains information of received message
    """
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