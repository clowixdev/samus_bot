from telebot.types import Message

from database.msg_templates import REPLIES
from database.dbworker import get_user, gen_users, add_rr_name, update_templates, get_templates, delete_template, get_usernames

from loader import bot, engine, secret_word, DEVS, ADMINS

def gen_templates() -> str:
    """Function that generates one entire message with templates

    Returns:
        str: Generated message
    """
    message = 'Ваши шаблоны:\n\n'
    current_templates = get_templates(engine)
    for keys in current_templates:
        formatted_template = ''
        for word in str.split(current_templates[keys]):
            if word == '{rr_name}':
                formatted_template += 'имя_соклановца'
            elif word[:-1] == '{rr_name}':
                formatted_template += 'имя_соклановца' + word[-1]
            else:
                formatted_template += word
            formatted_template += ' '
        formatted_template = str.rstrip(formatted_template)
        message += f"{keys+1}) {formatted_template}\n\n"

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