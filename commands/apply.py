from telebot.types import Message, ReplyKeyboardRemove, InputMediaPhoto, CallbackQuery
from datetime import datetime
from typing import List

from time import sleep

from database.msg_templates import REPLIES
from database.dbworker import get_user

from loader import bot, appliances, admins_chat_id, general_chat_link, engine, media_groups

from functions.funcs import stop_talking, have_username
from functions.keyboards import create_check_markup, create_stop_markup, create_requirements_markup, create_welcome_markup, create_unlogged_markup, create_accept_markup
from functions.decorators import chat_required, spam_checker

from .register import register_command


@bot.message_handler(commands=["start"])
@bot.message_handler(func=lambda message: message.text == "Начать ⭐")
@spam_checker
@chat_required
def start_command(message: Message)-> None:
    """Handler that provides work of "/start" command.

    Args:
        message (Message): Object, that contains information of received message
    """
    bot.reply_to(message, REPLIES["start"])
    curr_user = get_user(message.from_user.id, None, engine)
    if curr_user != None:
        message.text = "/register"
        sleep(0.3)
        register_command(message)
        return
    bot.reply_to(message, REPLIES["welcome"], reply_markup=create_welcome_markup())
    print("{date} {username} with id {id} called \"/start\" in {chat_id}".format(date=datetime.now(), username=message.from_user.username, id=message.from_user.id, chat_id=message.chat.id))


@bot.message_handler(commands=["apply"])
@bot.message_handler(func=lambda message: message.text == "Подать заявку 📨")
@spam_checker
@chat_required
def apply_command(message: Message)-> None:
    """Handler that provides work of "/apply" command.

    Args:
        message (Message): Object, that contains information of received message
    """
    if stop_talking(message):
        return
    
    curr_user = get_user(message.from_user.id, None, engine)
    if curr_user != None:
        message.text = "/register"
        sleep(0.3)
        register_command(message)
        return
    
    if not have_username(message):
        bot.reply_to(message, REPLIES["add_username"], reply_markup=create_unlogged_markup())
        return

    bot.reply_to(message, REPLIES["apply_message"], reply_markup=create_requirements_markup())
    bot.register_next_step_handler(message, acceptance_command)

    print("{date} {username} with id {id} called \"/apply\" in {chat_id}".format(date=datetime.now(), username=message.from_user.username, id=message.from_user.id, chat_id=message.chat.id))


def acceptance_command(message: Message)-> None:
    """Handler that provides work to negative answer for a requirements.

    Args:
        message (Message): Object, that contains information of received message
    """
    if stop_talking(message):
        return
    
    if message.text == "Не согласен ❌":
        bot.reply_to(message, REPLIES["deny_req_message"], reply_markup=ReplyKeyboardRemove())
        print("{date} {username} with id {id} called \"denied requirements\" in {chat_id}".format(date=datetime.now(), username=message.from_user.username, id=message.from_user.id, chat_id=message.chat.id))
    elif message.text == "Согласен ✅":
        bot.reply_to(message, REPLIES["accept_req_message"])
        bot.reply_to(message, REPLIES["create_appliance_photos"], reply_markup=create_stop_markup())

        media_groups[message.from_user.id] = []
        
        bot.register_next_step_handler(message, create_appliance_photos_command)
        print("{date} {username} with id {id} accepted requirements in {chat_id}".format(date=datetime.now(), username=message.from_user.username, id=message.from_user.id, chat_id=message.chat.id))


def create_appliance_photos_command(message: Message)-> None:
    """Handler that provides work to positive answer for a requirements and ask for photos of account

    Args:
        message (Message): Object, that contains information of received message
    """
    if stop_talking(message):
        return
    
    if message.content_type != "photo":
        bot.reply_to(message, REPLIES["photos_required"])
        message.text = "Согласен ✅"
        acceptance_command(message)
        return
    
    photo_info = bot.get_file(message.photo[-1].file_id)
    photo_bytes = bot.download_file(photo_info.file_path)
    media_groups[message.from_user.id] += [photo_bytes]

    bot.reply_to(message, REPLIES["create_appliance_bio"], reply_markup=create_stop_markup())
    bot.register_next_step_handler(message, create_appliance_bio_command)

    print("{date} {username} with id {id} is confirming appliance in {chat_id}".format(date=datetime.now(), username=message.from_user.username, id=message.from_user.id, chat_id=message.chat.id))


def create_appliance_bio_command(message: Message) -> None:
    """This handler will ask user to type some information about him

    Args:
        message (Message): Object, that contains information of received message
    """
    if stop_talking(message):
        return
    
    if message.content_type != "text":
        bot.reply_to(message, REPLIES["bio_required"])
        message.text = "Согласен ✅"
        acceptance_command(message)
        return

    appliances[message.from_user.id] = []

    appliances[message.from_user.id].append(REPLIES["appliance"].format(
        bio=message.caption or message.text,
        username=message.from_user.username
        ))
    
    appliance_message = [
        InputMediaPhoto(media_groups[message.from_user.id][0], 
                        caption=appliances[message.from_user.id][0]),
    ]

    appliances[message.from_user.id].pop(0)
    media_groups[message.from_user.id].pop(0)

    for photo in media_groups[message.from_user.id]:
        appliance_message += [InputMediaPhoto(photo)]

    try:
        bot.send_media_group(message.from_user.id, appliance_message)
    except Exception as e:
        bot.reply_to(message, REPLIES["bio_too_long"])
        bot.reply_to(message, REPLIES["create_appliance_bio"], reply_markup=create_stop_markup())
        bot.register_next_step_handler(message, create_appliance_bio_command)
        return

    bot.reply_to(message, REPLIES["check_appliance"], reply_markup=create_check_markup())
    bot.register_next_step_handler(message, check_appliance_command, appliance_message)


def check_appliance_command(message: Message, appliance_message: List) -> None:
    """Handler that provides work to positive answer for a requirements.

    Args:
        message (Message): Object, that contains information of received message
    """
    if stop_talking(message):
        return
    
    if message.text == "Верно ✅":
        bot.send_media_group(admins_chat_id, appliance_message)
        appliance_message_id = bot.send_message(admins_chat_id, REPLIES["message_for_inline"], reply_markup=create_accept_markup(message.from_user.id)).message_id
        appliances[message.from_user.id] = [appliance_message, appliance_message_id]
        bot.reply_to(message, REPLIES["appliance_sent"], reply_markup=ReplyKeyboardRemove())
    elif message.text == "Не верно ❌":
        bot.reply_to(message, REPLIES["redo_appliance"], reply_markup=ReplyKeyboardRemove())
        message.text = "Согласен ✅"
        acceptance_command(message)
        return

    print("{date} {username} with id {id} SENT APPLIANCE in {chat_id}".format(date=datetime.now(), username=message.from_user.username, id=message.from_user.id, chat_id=message.chat.id))


@bot.callback_query_handler(func=lambda callback: callback.data[0] == "a")
def accept_button(callback: CallbackQuery) -> None:
    """Callback query handler that will handle positive answer from an admins of clan

    Args:
        callback (CallbackQuery): Object that containts all information about sent data
    """
    applicant_id = int(callback.data[1:])
    bot.edit_message_text(
        text=callback.message.text + REPLIES["appliance_accepted"].format(username=callback.from_user.username),
        chat_id=admins_chat_id,
        message_id=appliances[applicant_id][1]
        )
    del(appliances[applicant_id], media_groups[applicant_id])

    bot.send_message(applicant_id, REPLIES["answer_accepted"].format(
        link=general_chat_link
    ), reply_markup=create_unlogged_markup())


@bot.callback_query_handler(func=lambda callback: callback.data[0] == "d")
def deny_button(callback: CallbackQuery) -> None:
    """Callback query handler that will handle negative answer from an admins of clan

    Args:
        callback (CallbackQuery): Object that containts all information about sent data
    """
    applicant_id = int(callback.data[1:])
    bot.edit_message_text(
        text=callback.message.text + REPLIES["appliance_rejected"].format(username=callback.from_user.username),
        chat_id=admins_chat_id,
        message_id=appliances[applicant_id][1]
        )
    del(appliances[applicant_id], media_groups[applicant_id])

    bot.send_message(applicant_id, REPLIES["answer_rejected"], reply_markup=ReplyKeyboardRemove())

    print("{date} {username} with id {id} rejected in {chat_id}".format(date=datetime.now(), username=callback.message.from_user.username, id=callback.message.from_user.id, chat_id=callback.message.chat.id))
