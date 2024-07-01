from telebot.types import Message, PollAnswer
from datetime import datetime

from loader import bot, engine

from database.msg_templates import REPLIES
from database.dbworker import edit_user_rrname, edit_user_critdmg, edit_user_uid, edit_user_platform, edit_user_fractions, edit_user_pawns

from functions.decorators import chat_required, member_required, spam_checker
from functions.funcs import stop_talking, check_uid, check_critdmg, check_platform, create_dragon_poll, create_pawns_poll
from functions.keyboards import create_edit_markup, create_stop_markup, create_start_markup

polls = dict()

@bot.message_handler(commands=["edit"])
@bot.message_handler(func=lambda message: message.text == "Изменить профиль ✏️")
@spam_checker
@chat_required
@member_required
def profile_edit_command(message: Message)-> None:
    """Handler, that will provide an editing of player profile

    Args:
        message (Message): Object, that contains information of received message
    """

    bot.reply_to(message, REPLIES["edit_profile"], reply_markup=create_edit_markup())

    print("{date} {username} with id {id} called \"/edit\" in {chat_id}".format(date=datetime.now(), username=message.from_user.username, id=message.from_user.id, chat_id=message.chat.id))


@bot.message_handler(func=lambda message: message.text == "Никнейм 🪪")
@spam_checker
@chat_required
@member_required
def edit_name_handler(message: Message) -> None:
    """Handler that will help user to edit his nickname

    Args:
        message (Message): Object, that contains information of received message
    """
    bot.reply_to(message, REPLIES["edit_nickname"], reply_markup=create_stop_markup())
    bot.register_next_step_handler(message, edit_nickname)


def edit_nickname(message: Message) -> None:
    """Function, that will format a new name and change it in database

    Args:
        message (Message): Object, that contains information of received message
    """

    if stop_talking(message):
        return
    
    new_name = message.text.strip()
    edit_user_rrname(new_name, message.from_user.id, engine)

    bot.reply_to(message, REPLIES["edit_nickname_ok"], reply_markup=create_start_markup(message.from_user.id))


@bot.message_handler(func=lambda message: message.text == "Крит. урон 🔪")
@spam_checker
@chat_required
@member_required
def edit_crit_handler(message: Message) -> None:
    """Handler that will help user to edit his crit damage

    Args:
        message (Message): Object, that contains information of received message
    """
    bot.reply_to(message, REPLIES["edit_crit"], reply_markup=create_stop_markup())
    bot.register_next_step_handler(message, edit_crit)


def edit_crit(message: Message) -> None:
    """Function that will change a user's crit damage in database

    Args:
        message (Message): Object, that contains information of received message
        
    """

    if stop_talking(message):
        return

    try:
        check_critdmg(int(message.text))
        edit_user_critdmg(int(message.text), message.from_user.id, engine)
        bot.reply_to(message, REPLIES["edit_crit_ok"], reply_markup=create_start_markup(message.from_user.id))
    except ValueError as e:
        bot.reply_to(message, REPLIES["invalid_critdmg"], reply_markup=create_stop_markup())
        edit_crit_handler(message)
        return


@bot.message_handler(func=lambda message: message.text == "UID 📄")
@spam_checker
@chat_required
@member_required
def edit_uid_handler(message: Message) -> None:
    """Handler that will help user to edit his UID

    Args:
        message (Message): Object, that contains information of received message
    """
    bot.reply_to(message, REPLIES["edit_uid"], reply_markup=create_stop_markup())
    bot.register_next_step_handler(message, edit_uid)


def edit_uid(message: Message) -> None:
    """Function that will edit user's UID in database

    Args:
        message (Message): Object, that contains information of received message
    """

    if stop_talking(message):
        return

    try:
        check_uid(int(message.text))
        edit_user_uid(int(message.text), message.from_user.id, engine)
        bot.reply_to(message, REPLIES["edit_uid_ok"], reply_markup=create_start_markup(message.from_user.id))
    except ValueError as e:
        bot.reply_to(message, REPLIES["invalid_uid"], reply_markup=create_stop_markup())
        edit_uid_handler(message)
        return


@bot.message_handler(func=lambda message: message.text == "Платформа 📱")
@spam_checker
@chat_required
@member_required
def edit_platform_handler(message: Message) -> None:
    """Handler that will help user to edit his platform

    Args:
        message (Message): Object, that contains information of received message
    """
    bot.reply_to(message, REPLIES["edit_platform"], reply_markup=create_stop_markup())
    bot.register_next_step_handler(message, edit_platform)


def edit_platform(message: Message) -> None:
    """Function that will change user's platform in database

    Args:
        message (Message): Object, that contains information of received message
    """
    try:
        check_platform(message.text)
        edit_user_platform(message.text, message.from_user.id, engine)
        bot.reply_to(message, REPLIES["edit_platform_ok"], reply_markup=create_start_markup(message.from_user.id))
    except ValueError as e:
        bot.reply_to(message, REPLIES["invalid_platform"], reply_markup=create_stop_markup())
        edit_platform_handler(message)
        return

@bot.message_handler(func=lambda message: message.text == "Фракции в драконе 🔮")
@spam_checker
@chat_required
@member_required
def edit_fractions_handler(message: Message) -> None:
    """Handler that will help user to edit his fractions for dragon

    Args:
        message (Message): Object, that contains information of received message
    """
    bot.reply_to(message, REPLIES["edit_fractions"], reply_markup=create_stop_markup())
    poll = create_dragon_poll()
    poll_id = bot.send_poll(message.from_user.id, poll["question"], options=poll["options"], \
            is_anonymous=poll["is_anonymous"], allows_multiple_answers=poll["allow_multiple"])
    polls[message.from_user.id] = [poll["question"], poll_id.message_id]


def edit_fractions(poll_answers: list, user_id: int) -> None:
    """Function that will edit user's fractions in dragon in database

    Args:
        poll_data (list): list of choosen fractions
        user_id (int): user telegram id
    """
    edit_user_fractions(poll_answers, user_id, engine)
    bot.send_message(user_id, REPLIES["edit_fractions_ok"], reply_markup=create_start_markup(user_id))


@bot.message_handler(func=lambda message: message.text == "Особые пешки 🎉")
@spam_checker
@chat_required
@member_required
def edit_pawns_handler(message: Message) -> None:
    """Handler that will help user to edit his pawns for dragon

    Args:
        message (Message): Object, that contains information of received message
    """
    bot.reply_to(message, REPLIES["edit_pawns"], reply_markup=create_stop_markup())
    poll = create_pawns_poll()
    poll_id = bot.send_poll(message.from_user.id, poll["question"], options=poll["options"], \
            is_anonymous=poll["is_anonymous"], allows_multiple_answers=poll["allow_multiple"])
    polls[message.from_user.id] = [poll["question"], poll_id.message_id]


def edit_pawns(poll_answers: list, user_id: int) -> None:
    """Function that will edit user's pawns in dragon in database

    Args:
        poll_data (list): list of choosen pawns
        user_id (int): user telegram id
    """
    edit_user_pawns(poll_answers, user_id, engine)
    bot.send_message(user_id, REPLIES["edit_pawns_ok"], reply_markup=create_start_markup(user_id))


@bot.poll_answer_handler()
def edit_polls(pollAnswer: PollAnswer) -> None:
    """This function will catch the poll answers and redirect it to correct functions

    Args:
        pollAnswer (PollAnswer): Object, that contains information about catched poll
        poll_question (str): poll question
    """
    dragon_poll_question = create_dragon_poll()["question"]
    pawn_poll_question = create_pawns_poll()["question"]

    bot.delete_message(pollAnswer.user.id, polls[pollAnswer.user.id][1])
    if polls[pollAnswer.user.id][0] == dragon_poll_question:
        edit_fractions(pollAnswer.option_ids, pollAnswer.user.id)
    elif polls[pollAnswer.user.id][0] == pawn_poll_question:
        edit_pawns(pollAnswer.option_ids, pollAnswer.user.id)

    del(polls[pollAnswer.user.id])


@bot.message_handler(func=lambda message: message.text == "Ничего ❌")
@spam_checker
@chat_required
@member_required
def edit_nothing_handler(message: Message) -> None:
    """Handler that will help user not to edit any attributes of his profile

    Args:
        message (Message): Object, that contains information of received message
    """
    bot.reply_to(message, REPLIES["edit_nothing"], reply_markup=create_start_markup(message.from_user.id))