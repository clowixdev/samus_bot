from telebot.types import Message, PollAnswer
from datetime import datetime

from database.msg_templates import REPLIES
from database.dbworker import get_user, add_user

from loader import bot, engine, secret_word

from functions.funcs import stop_talking, check_platform, check_critdmg, check_uid, create_dragon_poll, create_pawns_poll
from functions.keyboards import create_start_markup, create_stop_markup, create_unlogged_markup
from functions.decorators import chat_required, spam_checker

userdata = []

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
    curr_user = get_user(message.from_user.id, message.from_user.username, engine)
    if curr_user == None:
        bot.reply_to(message, REPLIES["authenticate"], reply_markup=create_stop_markup())
        bot.register_next_step_handler(message, auth_member)
    else:
        bot.reply_to(message, REPLIES["logged"].format(rr_name=curr_user.rr_name), reply_markup=create_start_markup(message.from_user.id))

    print("{date} {username} with id {id} called \"/start\" in {chat_id}".format(date=datetime.now(), username=message.from_user.username, id=message.from_user.id, chat_id=message.chat.id))


def auth_member(message: Message) -> None:
    """Handler that will check if user is a member of clan

    Args:
        message (Message): Object, that contains information of received message
    """

    if stop_talking(message):
        return

    if message.text == secret_word:
        bot.reply_to(message, REPLIES["add_nickname"], reply_markup=create_stop_markup())
        bot.register_next_step_handler(message, add_nickname)
    else:
        bot.reply_to(message, REPLIES["auth_failed"], reply_markup=create_unlogged_markup())
        print(f"auth failed by {message.from_user.username}")
        bot.register_next_step_handler(message, auth_member)


def add_nickname(message: Message) -> None:
    """Handler that will add users to database and also add their ingame nickname

    Args:
        message (Message): Object, that contains information of received message
    """

    if stop_talking(message):
        return
    
    global userdata
    if len(userdata) == 0:
        userdata.append(message.text)
        userdata.append(message.from_user.username)
    bot.reply_to(message, REPLIES["add_critdmg"], reply_markup=create_stop_markup())
    bot.register_next_step_handler(message, add_critdmg, userdata)


def add_critdmg(message: Message, userdata: list) -> None:
    """Handler that will collect data about crit DMG

    Args:
        message (Message): Object, that contains information of received message
        userdata (list): Stored data about player (format: [player_id, playername, username, critdmg, uid, platform, [fractions]])
    """

    if stop_talking(message):
        return
    
    try:
        if len(userdata) == 2:
            check_critdmg(int(message.text))
            userdata.append(int(message.text))
        bot.reply_to(message, REPLIES["add_uid"], reply_markup=create_stop_markup())
        bot.register_next_step_handler(message, add_uid, userdata)
    except ValueError as e:
        bot.reply_to(message, REPLIES["invalid_critdmg"], reply_markup=create_stop_markup())
        add_nickname(message)
        return


def add_uid(message: Message, userdata: list) -> None:
    """Handler that will collect data about uid

    Args:
        message (Message): Object, that contains information of received message
        userdata (list): Stored data about player (format: [player_id, playername, username, critdmg, uid, platform, [fractions]])
    """

    if stop_talking(message):
        return
    
    try:
        if len(userdata) == 3:
            check_uid(int(message.text))
            userdata.append(int(message.text))
        bot.reply_to(message, REPLIES["add_platform"], reply_markup=create_stop_markup())
        bot.register_next_step_handler(message, add_platform, userdata)
    except ValueError as e:
        bot.reply_to(message, REPLIES["invalid_uid"], reply_markup=create_stop_markup())
        add_critdmg(message, userdata)
        return


def add_platform(message: Message, userdata: list) -> None:
    """Handler that will collect data about users platform

    Args:
        message (Message): Object, that contains information of received message
        userdata (list): Stored data about player (format: [player_id, playername, username, critdmg, uid, platform, [fractions]])
    """

    if stop_talking(message):
        return

    try:
        if len(userdata) == 4:
            check_platform(message.text.strip())
            userdata.append(message.text.strip())

            poll = create_dragon_poll()
            poll_id = bot.send_poll(message.from_user.id, poll["question"], options=poll["options"], \
                        is_anonymous=poll["is_anonymous"], allows_multiple_answers=poll["allow_multiple"]).message_id
            
            userdata.insert(0, poll_id)
            userdata.insert(1, message.from_user.id)
    except ValueError as e:
        bot.reply_to(message, REPLIES["invalid_platform"], reply_markup=create_stop_markup())
        add_uid(message, userdata)
        return


@bot.poll_answer_handler()
def add_poll_data(pollAnswer: PollAnswer) -> None:
    """Handler that will get all the answers and pass data to the next handler

    Args:
        message (Message): Object, that contains information of received message
        userdata (list): Stored data about player (format: [player_id, playername, username, critdmg, uid, platform, [fractions]])
    """
    userdata.append(pollAnswer.option_ids)
    if len(userdata) == 8:
        add_fractions(userdata)
    else:
        add_event_pawns(userdata)


def add_fractions(userdata: list) -> None:
    """Handler that will create a poll and determine players fractions, then add all stored data to database

    Args:
        message (Message): Object, that contains information of received message
        userdata (list): Stored data about player (format: [player_id, playername, username, critdmg, uid, platform, [fractions]])
    """
    bot.delete_message(userdata[1], userdata[0])
    userdata.pop(0)

    poll = create_pawns_poll()
    poll_id = bot.send_poll(userdata[0], poll["question"], options=poll["options"], \
                is_anonymous=poll["is_anonymous"], allows_multiple_answers=poll["allow_multiple"]).message_id
    
    userdata.insert(0, poll_id)


def add_event_pawns(userdata: list) -> None:
    """Handler that will create a poll and determine players event pawns, then add all stored data to database

    Args:
        message (Message): Object, that contains information of received message
        userdata (list): Stored data about player (format: [player_id, playername, username, critdmg, uid, platform, [fractions]])
    """
    bot.delete_message(userdata[1], userdata[0])
    userdata.pop(0)

    bot.send_message(userdata[0], REPLIES["registration_passed"], reply_markup=create_start_markup(userdata[0]))
    bot.send_message(userdata[0], REPLIES["logged"].format(rr_name=userdata[1]), reply_markup=create_start_markup(userdata[0]))

    add_user(userdata, engine)

