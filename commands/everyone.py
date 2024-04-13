from telebot.types import Message

from database.msg_templates import REPLIES
from database.dbworker import get_user, gen_users, add_rr_name, update_templates, get_templates, delete_template, get_usernames

from loader import bot, engine, secret_word, DEVS, ADMINS

from functions.funcs import in_group, stop_talking, gen_templates


@bot.message_handler(commands=['everyone'])
def mention_all(message: Message) -> None:
    """This command will mention all registered users in database

    Args:
        message (Message): Object, that contains information of received message
    """

    if message.from_user.id != message.chat.id:
        mention_message = ''
        all_usernames = get_usernames(engine)
        for username in all_usernames:
            mention_message += f'@{username} '
        mention_message = str.rstrip(mention_message)
        mention_message += REPLIES['after_everyone']
        bot.send_message(message.chat.id, mention_message)
    else:
        bot.reply_to(message, REPLIES['only_for_chat'])

    print("{username} with id {id} called '/everyone' in {chat_id}".format(username=message.from_user.username, id=message.from_user.id, chat_id=message.chat.id))