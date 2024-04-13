from telebot.types import Message

from database.msg_templates import REPLIES
from database.dbworker import get_user, gen_users, add_rr_name, update_templates, get_templates, delete_template, get_usernames

from loader import bot, engine, secret_word, DEVS, ADMINS

from functions.funcs import in_group, stop_talking, gen_templates


@bot.message_handler(commands=['all'])
def handle_all(message: Message) -> None:
    """Handler that allows leaders to contact all clan members

    Args:
        message (Message): Object, that contains information of received message
    """
    if in_group(message):
        return
    
    if message.from_user.id in DEVS:
        bot.reply_to(message, REPLIES['choose_template'])
        bot.reply_to(message, gen_templates())
        bot.register_next_step_handler(message, choose_template)
    else:
        print("Permission error")

    print("{username} with id {id} called '/all' in {chat_id}".format(username=message.from_user.username, id=message.from_user.id, chat_id=message.chat.id))


def choose_template(message: Message) -> None:
    """Handler that will send choosen template to all members of the clan

    Args:
        message (Message): Object, that contains information of received message
        template_id (int): ID of choosen template
    """

    if stop_talking(message):
        return
    
    if message.text == '0':
        bot.send_message(message.from_user.id, REPLIES['send_without_storing'])
        bot.register_next_step_handler(message, send_without_storing)
    
    templates = get_templates(engine)
    try:
        template_id = int(message.text) - 1
    except ValueError as e:
        bot.reply_to(message, REPLIES['invalid_key'])
        handle_all(message)
        return

    for user in gen_users(engine):
        if user.id == message.from_user.id:
            bot.send_message(user.id, templates[template_id].format(rr_name=user.rr_name))
            continue
        else:
            try:
                bot.send_message(user.id, templates[template_id].format(rr_name=user.rr_name))
            except KeyError as e:
                print(e)
                bot.reply_to(message, REPLIES['invalid_key'])
                handle_all(message)
                return
    bot.send_message(message.from_user.id, REPLIES['msg_sent'])


def send_without_storing(message: Message) -> None:
    """This handler will allow leader to send message right now without saving it

    Args:
        message (Message): Object, that contains information of received message
    """
    for user in gen_users(engine):
        if user.id == message.from_user.id:
            bot.send_message(user.id, message.text)
            continue
        else:
            bot.send_message(user.id, message.text)
    bot.send_message(message.from_user.id, REPLIES['msg_sent'])