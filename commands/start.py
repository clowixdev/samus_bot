from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from database.msg_templates import REPLIES
from database.dbworker import get_user, gen_users, add_rr_name, update_templates, get_templates, delete_template, get_usernames

from loader import bot, engine, dev_id, leader_id, secret_word

# DEVS = [int(dev_id), int(leader_id)]
DEVS = [int(dev_id)]
ALPHABET = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

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

@bot.message_handler(commands=['start'])
def start_command(message: Message)-> None:
    """Handler that provides work of "/start" command.

    Args:
        message (Message): Object, that contains information of received message
    """

    if in_group(message):
        return

    bot.reply_to(message, REPLIES['start'])
    curr_user_rr_name = get_user(message.from_user.id, message.from_user.username, engine)
    if curr_user_rr_name == '_empty_name_':
        bot.reply_to(message, REPLIES['register'])
        bot.register_next_step_handler(message, register_user)
    else:
        bot.reply_to(message, REPLIES['logged'].format(rr_name=curr_user_rr_name))
        bot.reply_to(message, REPLIES['commands'])

    print("{username} with id {id} called '/start' in {chat_id}".format(username=message.from_user.username, id=message.from_user.id, chat_id=message.chat.id))


def register_user(message: Message) -> None:
    """Handler that will add users to database and also add their ingame nickname

    Args:
        message (Message): Object, that contains information of received message
    """

    if stop_talking(message):
        return

    bot.reply_to(message, REPLIES['authenticate'])
    bot.register_next_step_handler(message, auth_member, username=message.text)


def auth_member(message: Message, username: str) -> None:
    """Handler that will check if user is a member of clan

    Args:
        message (Message): Object, that contains information of received message
    """

    if stop_talking(message):
        return

    if message.text == secret_word:
        user = get_user(message.from_user.id, message.from_user.username, engine)
        if user:
            add_rr_name(message.from_user.id, message.from_user.username, username, engine)
            bot.reply_to(message, REPLIES['auth_passed'])
        else:
            print("Error occured while getting user from db")
    else:
        bot.reply_to(message, REPLIES['auth_failed'])
        print(f"auth failed by {message.from_user.username}")


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


@bot.message_handler(commands=['new'])
def handle_new(message: Message) -> None:
    """Handler that can help leader add his own templates

    Args:
        message (Message): Object, that contains information of received message
    """

    if in_group(message):
        return

    bot.reply_to(message, REPLIES['add_template'])
    bot.register_next_step_handler(message, add_template)

    print("{username} with id {id} called '/new' in {chat_id}".format(username=message.from_user.username, id=message.from_user.id, chat_id=message.chat.id))


def add_template(message: Message) -> None:
    """Function that add leader template

    Args:
        message (Message): Object, that contains information of received message
    """

    if stop_talking(message):
        return
    
    user_template = ''

    for word in str.split(message.text):
        if 'имя_игрока' in word:
            user_template += "{rr_name}"
            if word[-1].lower() not in ALPHABET:
                user_template += word[-1]
        else:
            user_template += word
        user_template += ' '
    
    user_template = str.rstrip(user_template)

    last_key = ''
    new_template_id = 0
    templates = get_templates(engine)
    try:
        for key in templates:
            last_key = key
        new_template_id = str(last_key + 1)
    except Exception as e:
        print(e)

    update_templates(user_template, new_template_id, engine)
    bot.reply_to(message, REPLIES['template_created'])


@bot.message_handler(commands=['del'])
def handle_del(message: Message) -> None:
    """Handler that can help leader del added templates

    Args:
        message (Message): Object, that contains information of received message
    """

    if in_group(message):
        return

    bot.reply_to(message, gen_templates())
    bot.reply_to(message, REPLIES['del_template'])
    bot.register_next_step_handler(message, del_template)

    print("{username} with id {id} called '/del' in {chat_id}".format(username=message.from_user.username, id=message.from_user.id, chat_id=message.chat.id))


def del_template(message: Message) -> None:
    """Function that add leader template

    Args:
        message (Message): Object, that contains information of received message
    """

    if stop_talking(message):
        return

    try:
        template_id = int(message.text) - 1
    except ValueError as e:
        bot.reply_to(message, REPLIES['invalid_key'])
        handle_del(message)
        return

    try:
        delete_template(template_id, engine)
        bot.reply_to(message, REPLIES['template_deleted'])
    except KeyError as e:
        bot.reply_to(message, REPLIES['invalid_key'])
        handle_del(message)
        return



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


@bot.message_handler(commands=['help'])
def help_command(message: Message) -> None:
    """Handler that will send to user list of command that he provides

    Args:
        message (Message): Object, that contains information of received message
    """
    bot.reply_to(message, REPLIES['help'])
    bot.reply_to(message, REPLIES['commands'])


@bot.message_handler(func=lambda _: True)
def incorrect_command(message: Message) -> None:
    """Handler that provides work with synonims of the word "Hello" 
    to greet the user and notify him that he is doing something wrong.

    Args:
        message (Message): Object, that contains information of received message
    """
    if message.chat.id == message.from_user.id:
        bot.reply_to(message, REPLIES['incorrect'])