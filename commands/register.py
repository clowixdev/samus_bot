from telebot.types import Message, PollAnswer
from datetime import datetime

from database.msg_templates import REPLIES
from database.dbworker import get_user, add_user

from loader import bot, engine, secret_word, current_polls, userdata

from functions.funcs import stop_talking, check_platform, check_critdmg, check_uid, create_dragon_poll, create_pawns_poll, have_username
from functions.keyboards import create_start_markup, create_stop_markup, create_unlogged_markup
from functions.decorators import chat_required, spam_checker


@bot.message_handler(commands=["register"])
@bot.message_handler(func=lambda message: message.text == "Уже участник 🔍")
@spam_checker
@chat_required
def register_command(message: Message)-> None:
    """Handler that provides work of "/register" command.

    Args:
        message (Message): Object, that contains information of received message
    """
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
    
    if not have_username(message):
        bot.reply_to(message, REPLIES["add_username"], reply_markup=create_unlogged_markup())
        return

    if message.text == secret_word:
        userdata[message.from_user.id] = []
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
    
    if len(userdata[message.from_user.id]) == 0:
        userdata[message.from_user.id].append(message.text)
        userdata[message.from_user.id].append(message.from_user.username)
    bot.reply_to(message, REPLIES["add_critdmg"], reply_markup=create_stop_markup())
    bot.register_next_step_handler(message, add_critdmg)


def add_critdmg(message: Message) -> None:
    """Handler that will collect data about crit DMG

    Args:
        message (Message): Object, that contains information of received message
    """

    if stop_talking(message):
        return
    
    try:
        if len(userdata[message.from_user.id]) == 2:
            check_critdmg(int(message.text))
            userdata[message.from_user.id].append(int(message.text))
        bot.reply_to(message, REPLIES["add_uid"], reply_markup=create_stop_markup())
        bot.register_next_step_handler(message, add_uid)
    except ValueError as e:
        bot.reply_to(message, REPLIES["invalid_critdmg"], reply_markup=create_stop_markup())
        add_nickname(message)
        return


def add_uid(message: Message) -> None:
    """Handler that will collect data about uid

    Args:
        message (Message): Object, that contains information of received message
    """

    if stop_talking(message):
        return
    
    try:
        if len(userdata[message.from_user.id]) == 3:
            check_uid(int(message.text))
            userdata[message.from_user.id].append(int(message.text))
        bot.reply_to(message, REPLIES["add_platform"], reply_markup=create_stop_markup())
        bot.register_next_step_handler(message, add_platform)
    except ValueError as e:
        bot.reply_to(message, REPLIES["invalid_uid"], reply_markup=create_stop_markup())
        add_critdmg(message)
        return


def add_platform(message: Message) -> None:
    """Handler that will collect data about users platform

    Args:
        message (Message): Object, that contains information of received message
    """

    if stop_talking(message):
        return

    try:
        if len(userdata[message.from_user.id]) == 4:
            check_platform(message.text.strip())
            userdata[message.from_user.id].append(message.text.strip())

            poll = create_dragon_poll()
            current_polls[message.from_user.id] = "start"
            poll_id = bot.send_poll(message.from_user.id, poll["question"], options=poll["options"], \
                        is_anonymous=poll["is_anonymous"], allows_multiple_answers=poll["allow_multiple"]).message_id
            
            userdata[message.from_user.id].insert(0, poll_id)
            userdata[message.from_user.id].insert(1, message.from_user.id)
    except ValueError as e:
        bot.reply_to(message, REPLIES["invalid_platform"], reply_markup=create_stop_markup())
        add_uid(message)
        return


def add_fractions(user_id: int) -> None:
    """Handler that will create a poll and determine players fractions, then add all stored data to database

    Args:
        user_id (int): user id that is defined by Telegram
    """
    bot.delete_message(userdata[user_id][1], userdata[user_id][0])
    userdata[user_id].pop(0)

    poll = create_pawns_poll()
    current_polls[user_id] = "start"
    poll_id = bot.send_poll(userdata[user_id][0], poll["question"], options=poll["options"], \
                is_anonymous=poll["is_anonymous"], allows_multiple_answers=poll["allow_multiple"]).message_id
    
    userdata[user_id].insert(0, poll_id)

@bot.poll_answer_handler(func=lambda pollAnswer: current_polls[pollAnswer.user.id] == "start")
def add_poll_data(pollAnswer: PollAnswer) -> None:
    """Handler that will get all the answers and pass data to the next handler

    Args:
        message (Message): Object, that contains information of received message
        userdata (list): Stored data about player (format: [player_id, playername, username, critdmg, uid, platform, [fractions]])
    """

    userdata[pollAnswer.user.id].append(pollAnswer.option_ids)
    if len(userdata[pollAnswer.user.id]) == 8:
        add_fractions(pollAnswer.user.id)
    else:
        add_event_pawns(pollAnswer.user.id)

def add_event_pawns(user_id: int) -> None:
    """Handler that will create a poll and determine players event pawns, then add all stored data to database

    Args:
        user_id (int): user id that is defined by Telegram
    """
    bot.delete_message(userdata[user_id][1], userdata[user_id][0])
    userdata[user_id].pop(0)

    bot.send_message(userdata[user_id][0], REPLIES["registration_passed"], reply_markup=create_start_markup(userdata[user_id][0]))
    bot.send_message(userdata[user_id][0], REPLIES["logged"].format(rr_name=userdata[user_id][1]), reply_markup=create_start_markup(userdata[user_id][0]))

    add_user(userdata[user_id], engine)
    del(userdata[user_id])

