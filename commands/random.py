from telebot.types import Message
from datetime import datetime
from random import randint

from database.msg_templates import REPLIES
from database.dbworker import delete_user

from loader import bot, engine

from functions.funcs import cut_numbers, check_border
from functions.decorators import group_required, admin_required, spam_checker

@bot.message_handler(commands=["random"])
@spam_checker
@group_required
@admin_required
def random_command(message: Message)-> None:
    """Handler that provides work of "/random <int>" command. This command will force
    bot to send random number between 1 and <int> to define the winner

    Args:
        message (Message): Object, that contains information of received message
    """
    try:
        right_border = cut_numbers(message.text)
        if right_border == None:
            raise ValueError
        
        right_border = check_border(right_border)
    except ValueError as e:
        bot.reply_to(message, REPLIES["random_error"])
        return

    winner_number = randint(1, right_border)
    bot.reply_to(message, REPLIES["random_winner"].format(participants=right_border, winner_number=winner_number))

    print("{date} {username} with id {id} called \"/random\" in {chat_id}".format(
        date=datetime.now(), 
        username=message.from_user.username, 
        id=message.from_user.id, 
        chat_id=message.chat.id
        ))    