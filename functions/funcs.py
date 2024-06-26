from typing import Tuple
from types import NoneType

from telebot.types import Message

from database.msg_templates import REPLIES
from database.dbworker import get_templates_descriptions, gen_users, get_template_by_id
from database.models import User, Template

from functions.keyboards import create_start_markup, create_unlogged_markup

from loader import bot, engine, ADMINS, DEVS

def is_member(message: Message) -> bool:
    """Function will check if user that sending messages is a member of a clan

    Args:
        message (Message): Object, that contains information of received message

    Returns:
        bool: True if user is a member and False if he is not
    """
    for user in gen_users(engine):
        if message.from_user.username == user.username:
            return True
    print(f"user with username @{message.from_user.username} and id {message.from_user.id} tried to use bot while unlogged")
    return False


def get_template(message: Message, recall_function: object) -> Template:
    """Function that handles all the errors while getting an template

    Args:
        message (Message): Object, that contains information of received message
        recall_function (object): function that will be called, if error is detected

    Returns:
        Template: model of a template
    """

    try:
        if len(message.text) == 1:
            template_id = int(message.text)
        else:
            template_id = int(message.text[-3])
    except ValueError as e:
        bot.reply_to(message, REPLIES["invalid_key"])
        recall_function(message)
        return
    
    template = get_template_by_id(template_id, engine)
    if template is None:
        bot.reply_to(message, REPLIES["invalid_key"])
        recall_function(message)
        return
    
    return template


def gen_templates() -> Tuple[str, int]:
    """Function that generates one entire message with templates

    Returns:
        str: Generated message
        int: Templates amount
    """
    message = "Все шаблоны:\n\n"
    current_templates = get_templates_descriptions(engine)
    
    if current_templates == {}:
        raise ValueError

    for keys in current_templates:
        formatted_template = ""
        for word in str.split(current_templates[keys]):
            if word == "{rr_name}":
                formatted_template += "имя_соклановца"
            elif word[:-1] == "{rr_name}":
                formatted_template += "имя_соклановца" + word[-1]
            else:
                formatted_template += word
            formatted_template += " "
        formatted_template = str.rstrip(formatted_template)
        message += f"{keys+1}) {formatted_template}\n\n"

    return (message, keys+1)


def stop_talking(message: Message) -> bool:
    """Function that provides exit from dialogue.

    Args:
        message (Message): Object, that contains information of received message

    Returns:
        bool: Returns true if message match "stop-word" else false
    """
    if type(message.text) != NoneType:
        if message.text.lower() == "стоп" or message.text == "Стоп ❌":
            bot.clear_step_handler_by_chat_id(message.chat.id)
            if is_member(message):
                bot.reply_to(message, REPLIES["stop"], reply_markup=create_start_markup(message.from_user.id))
            else:
                bot.reply_to(message, REPLIES["stop"], reply_markup=create_unlogged_markup())
            return True
        return False


def in_group(message: Message) -> bool:
    """Function that tells you whether bot called in group or not

    Args:
        message (Message): Object, that contains information of received message

    Returns:
        bool: Returns true if bot command was triggered in group else false
    """
    if message.from_user.id == message.chat.id:
        return False
    return True

def cut_username(string: str) -> str:
    """This function will find "@username" part of string and return it without "@"

    Args:
        string (str): given string

    Returns:
        str: telegram username without "@"
    """
    username = ""
    found_at = False
    for char in string:
        if char == "@":
            found_at = True
            continue
        if found_at:
            username += char
    
    if found_at == False: 
        return None
    return username


def check_platform(str: str) -> None:
    """Fucntion that will check correctness of inputed platform

    Args:
        str (str): message that will contain platform

    Raises:
        ValueError: raises ValueError in case platform is incorrect
    """
    if (str != "Android") and (str != "Iphone"):
        raise ValueError

def check_uid(uid: int) -> None:
    """Fucntion that will check correctness of inputed UID

    Args:
        str (str): message that will contain UID

    Raises:
        ValueError: raises ValueError in case UID is incorrect
    """
    if (uid < 10000000) or (uid > 99999999):
        raise ValueError


def check_critdmg(crit_dmg: int) -> None:
    """Fucntion that will check correctness of inputed CRIT. DMG

    Args:
        str (str): message that will contain CRIT. DMG

    Raises:
        ValueError: raises ValueError in case CRIT. DMG is incorrect
    """
    if (crit_dmg < 1) or (crit_dmg > 6853):
        raise ValueError
    

def create_dragon_poll() -> dict:
    """Function that generates dictionary with all settings for poll

    Returns:
        dict: poll settings dictionary
    """

    poll = dict()

    poll["question"] = REPLIES["add_fractions"]
    poll["options"] = [
        "Лесной союз 🍃",
        "Магический совет 🔮",
        "Королевство света ☀️",
        "Техногенное общество 💡",
        "Тёмные владения 🦇"
    ]
    poll["is_anonymous"] = False
    poll["allow_multiple"] = True

    return poll

def gen_fractions(user: User) -> str:
    """Function will generate fraction message

    Args:
        user (User): Object that stores all data about user

    Returns:
        str: message to implement into template
    """

    fraction_msg = ""
    if user.forest_fraction:
        fraction_msg += "Лесной союз 🍃\n"
    if user.magic_fraction:
        fraction_msg += "Магический совет 🔮\n"
    if user.light_fraction:
        fraction_msg += "Королевство света ☀️\n"
    if user.tech_fraction:
        fraction_msg += "Техногенное общество 💡\n"
    if user.dark_fraction:
        fraction_msg += "Тёмные владения 🦇"

    return fraction_msg


def is_admin(user_id: int) -> bool:
    """Function will decide whether player is admin or not

    Args:
        user_id (int): User ID that is defined by Telegram

    Returns:
        bool: True if player is admin or dev and False if vice-versa
    """
    if not (user_id in DEVS or user_id in ADMINS):
        return False
    else:
        return True