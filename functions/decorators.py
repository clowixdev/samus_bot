from functools import wraps
from datetime import datetime
from time import time

from typing import Callable, Any

from telebot.types import ReplyKeyboardRemove

from database.msg_templates import REPLIES
from database.dbworker import gen_users, is_blacklisted

from loader import bot, DEVS, ADMINS, engine, last_message, blacklist

from functions.keyboards import create_unlogged_markup


def chat_required(func: Callable) -> Any:
    """Function decorator that requires called function to be called in chat

    Args:
        func (Callable): decorated function

    Returns:
        Any: Result of decorated function call
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if args[0].from_user.id != args[0].chat.id:
            bot.reply_to(args[0], REPLIES["only_for_group"])
            return

        return func(*args, **kwargs)
    return wrapper


def group_required(func: Callable) -> Any:
    """Function decorator that requires called function to be called in group

    Args:
        func (Callable): decorated function

    Returns:
        Any: Result of decorated function call
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if args[0].from_user.id == args[0].chat.id:
            bot.reply_to(args[0], REPLIES["only_for_chat"])
            return

        return func(*args, **kwargs)
    return wrapper


def member_required(func: Callable) -> Any:
    """Function decorator that requires user to be an member of clan

    Args:
        func (Callable): decorated function

    Returns:
        Any: Result of decorated function call
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id_list = [user.id for user in gen_users(engine)]
        if args[0].from_user.id not in user_id_list:
            bot.reply_to(
                args[0], 
                REPLIES["not_logged"], 
                reply_markup=create_unlogged_markup(),
            )
            print(f"{datetime.now()} user with username @{args[0].from_user.username} and id {args[0].from_user.id} tried to use bot while unlogged")
            return
        
        return func(*args, **kwargs)
    return wrapper


def admin_required(func: Callable) -> Any:
    """Function decorator that requires user to be an admin of clan

    Args:
        func (Callable): decorated function

    Returns:
        Any: Result of decorated function call
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not (args[0].from_user.id in DEVS or args[0].from_user.id in ADMINS):
            bot.reply_to(
                args[0], 
                REPLIES["rights_required"], 
                reply_markup=ReplyKeyboardRemove(), 
            )
            return
        return func(*args, **kwargs)
    return wrapper


def spam_checker(func: Callable) -> Any:
    """Function decorator that will not handle message if it is spamming

    Args:
        func (Callable): decorated function

    Returns:
        Any: Result of decorated function call
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if is_blacklisted([args[0].from_user.id, args[0].from_user.username], blacklist):
            print(f"{datetime.now()} ({args[0].from_user.id} - {args[0].from_user.username}) is trying to chat while blacklisted")
            return

        if args[0].from_user.id not in last_message:
            last_message[args[0].from_user.id] = float(0)

        if (float(time()) - float(last_message[args[0].from_user.id])) < 0.3:
            return

        last_message[args[0].from_user.id] = float(time())
        return func(*args, **kwargs)
    return wrapper


def dev_required(func: Callable) -> Any:
    """Function decorator that requires user to be a dev

    Args:
        func (Callable): decorated function

    Returns:
        Any: Result of decorated function call
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not (args[0].from_user.id in DEVS):
            print("{date} {username} with id {id} called dev function with no rights in {chat_id}".format(
                date=datetime.now(), 
                username=args[0].from_user.username, 
                id=args[0].from_user.id, 
                chat_id=args[0].chat.id
            ))
            return
        return func(*args, **kwargs)
    return wrapper