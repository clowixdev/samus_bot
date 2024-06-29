from telebot.types import Message

from database.msg_templates import REPLIES
from database.dbworker import delete_template

from loader import bot, engine

from functions.funcs import stop_talking, gen_templates, get_template
from functions.keyboards import create_del_markup, create_start_markup
from functions.decorators import chat_required, member_required, admin_required


@bot.message_handler(commands=["del"])
@bot.message_handler(func=lambda message: message.text == "Удалить шаблон 🗑️")
@chat_required
@member_required
@admin_required
def delete_command(message: Message) -> None:
    """Handler that can help leader del added templates

    Args:
        message (Message): Object, that contains information of received message
    """

    try:
        templates, templates_amt = gen_templates()
        bot.reply_to(message, templates)
        bot.reply_to(message, REPLIES["del_template"], reply_markup=create_del_markup(templates_amt))
        bot.register_next_step_handler(message, del_template)
    except ValueError as e:
        bot.reply_to(message, REPLIES["empty_templates"], reply_markup=create_start_markup(message.from_user.id))

    print("{username} with id {id} called \"/del\" in {chat_id}".format(username=message.from_user.username, id=message.from_user.id, chat_id=message.chat.id))


def del_template(message: Message) -> None:
    """Function that add leader template

    Args:
        message (Message): Object, that contains information of received message
    """

    if stop_talking(message):
        return
    
    template = get_template(message, delete_command)

    try:
        delete_template(template.template, engine)
        bot.reply_to(message, REPLIES["template_deleted"], reply_markup=create_start_markup(message.from_user.id))
    except KeyError as e:
        bot.reply_to(message, REPLIES["invalid_key"])
        delete_command(message)
        return