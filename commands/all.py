from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from database.msg_templates import REPLIES
from database.dbworker import gen_users, get_templates

from loader import bot, engine, DEVS

from functions.funcs import in_group, stop_talking, gen_templates
from functions.keyboards import create_all_markup, create_start_markup


@bot.message_handler(commands=["all"])
@bot.message_handler(func=lambda message: message.text == "Рассылка клану 📨")
def handle_all(message: Message) -> None:
    """Handler that allows leaders to contact all clan members

    Args:
        message (Message): Object, that contains information of received message
    """
    if in_group(message):
        return
    
    if message.from_user.id in DEVS:
        bot.reply_to(message, REPLIES["choose_template"])
        templates, templates_amt = gen_templates()

        bot.reply_to(message, templates, reply_markup=create_all_markup(templates_amt))
        bot.register_next_step_handler(message, choose_template)
    else:
        print("Permission error")

    print("{username} with id {id} called \"/all\" in {chat_id}".format(username=message.from_user.username, id=message.from_user.id, chat_id=message.chat.id))


def choose_template(message: Message) -> None:
    """Handler that will send choosen template to all members of the clan

    Args:
        message (Message): Object, that contains information of received message
        template_id (int): ID of choosen template
    """

    if stop_talking(message):
        return
    
    if message.text == "Отправить без сохранения 📋" or message.text == "0":
        bot.send_message(message.from_user.id, REPLIES["send_without_storing"])
        bot.register_next_step_handler(message, send_without_storing)
    
    templates = get_templates(engine)
    try:
        template_id = int(message.text[-3]) - 1
    except ValueError as e:
        bot.reply_to(message, REPLIES["invalid_key"])
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
                bot.reply_to(message, REPLIES["invalid_key"])
                handle_all(message)
                return
    bot.send_message(message.from_user.id, REPLIES["msg_sent"], reply_markup=create_start_markup())


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
    bot.send_message(message.from_user.id, REPLIES["msg_sent"], reply_markup=create_start_markup())