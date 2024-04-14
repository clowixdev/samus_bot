from typing import Tuple

from telebot.types import Message

from database.msg_templates import REPLIES
from database.dbworker import get_templates

from functions.keyboards import create_start_markup

from loader import bot, engine


def gen_templates() -> Tuple[str, int]:
    """Function that generates one entire message with templates

    Returns:
        str: Generated message
    """
    message = "Ваши шаблоны:\n\n"
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
        bot.reply_to(message, REPLIES["stop"], reply_markup=create_start_markup())
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