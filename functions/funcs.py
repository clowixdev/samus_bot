from typing import Tuple

from telebot.types import Message

from database.msg_templates import REPLIES
from database.dbworker import get_templates, gen_users

from functions.keyboards import create_start_markup, create_unlogged_markup

from loader import bot, engine

def is_member(message: Message) -> bool:
    """Function will check if user that sending messages is a member of a clan

    Args:
        message (Message): message (Message): Object, that contains information of received message

    Returns:
        bool: True if user is a member and False if he is not
    """
    for user in gen_users(engine):
        if message.from_user.username == user.username:
            return True
    print(f"user with username @{message.from_user.username} tried to use bot while unlogged")
    return False



def gen_templates() -> Tuple[str, int]:
    """Function that generates one entire message with templates

    Returns:
        str: Generated message
    """
    message = "Все шаблоны:\n\n"
    current_templates = get_templates(engine)
    
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
    if message.text.lower() == "стоп" or message.text == "Стоп ❌":
        bot.clear_step_handler_by_chat_id(message.chat.id)
        if is_member(message):
            bot.reply_to(message, REPLIES["stop"], reply_markup=create_start_markup())
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