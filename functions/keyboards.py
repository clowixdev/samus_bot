from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from loader import DEVS, ADMINS

def create_start_markup(user_id: int) -> ReplyKeyboardMarkup:
    """Fucntion that will create ReplyKeyboard for "/start" command and return it
    
    Args:
        user_id (int): ID of user that is defined by telegram

    Returns:
        ReplyKeyboardMarkup: created markup for "/start" command
    """
    start_markup = ReplyKeyboardMarkup(resize_keyboard=True)

    all_button = KeyboardButton("Рассылка клану 📨")
    new_button = KeyboardButton("Создать шаблон 📝")
    del_button = KeyboardButton("Удалить шаблон 🗑️")
    view_button = KeyboardButton("Просмотреть шаблоны 👀")
    profile_button = KeyboardButton("Профиль 🪪")
    help_button = KeyboardButton("Помощь 📃")

    if (not user_id in DEVS) and (not user_id in ADMINS):
        start_markup.add(profile_button, help_button)
    else:
        start_markup.add(
            all_button, new_button, del_button, view_button, profile_button, help_button
        )

    return start_markup

def create_all_markup(templates_amt: int) -> ReplyKeyboardMarkup:
    """Fucntion that will create ReplyKeyboard for "/all" command and return it

    Args:
        templates_amt (int): amount of stored templates in database

    Returns:
        ReplyKeyboardMarkup: created markup for "/all" command
    """
    all_markup = ReplyKeyboardMarkup(resize_keyboard=True)

    for button in range(templates_amt):
        markup_button = KeyboardButton(f"Шаблон номер {button+1} 💾")
        all_markup.add(markup_button)

    instant_send_button = KeyboardButton("Отправить без сохранения 📋")
    stop_button = KeyboardButton("Стоп ❌")

    all_markup.add(instant_send_button, stop_button)

    return all_markup


def create_view_markup(templates_amt: int) -> ReplyKeyboardMarkup:
    """Fucntion that will create ReplyKeyboard for "/view" command and return it

    Args:
        templates_amt (int): amount of stored templates in database

    Returns:
        ReplyKeyboardMarkup: created markup for "/view" command
    """
    view_markup = ReplyKeyboardMarkup(resize_keyboard=True)

    for button in range(templates_amt):
        markup_button = KeyboardButton(f"Шаблон номер {button+1} 💾")
        view_markup.add(markup_button)

    stop_button = KeyboardButton("Стоп ❌")

    view_markup.add(stop_button)

    return view_markup


def create_del_markup(templates_amt: int) -> ReplyKeyboardMarkup:
    """Fucntion that will create ReplyKeyboard for "/del" command and return it

    Args:
        templates_amt (int): amount of stored templates in database

    Returns:
        ReplyKeyboardMarkup: created markup for "/del" command
    """
    del_markup = ReplyKeyboardMarkup(resize_keyboard=True)

    for button in range(templates_amt):
        markup_button = KeyboardButton(f"Шаблон номер {button+1} 💾")
        del_markup.add(markup_button)

    stop_button = KeyboardButton("Стоп ❌")

    del_markup.add(stop_button)

    return del_markup

def create_help_markup() -> ReplyKeyboardMarkup:
    """Fucntion that will create ReplyKeyboard for message that misses all the commands and return it

    Returns:
        ReplyKeyboardMarkup: created markup for missing command
    """
    help_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = KeyboardButton("Начать ⭐")
    help_button = KeyboardButton("Помощь 📃")
    help_markup.add(start_button, help_button)

    return help_markup

def create_stop_markup() -> ReplyKeyboardMarkup:
    """Fucntion that will create ReplyKeyboard with only 1 command, to stop dialogue and return it

    Returns:
        ReplyKeyboardMarkup: created markup for stopping dialogue
    """
    stop_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    stop_button = KeyboardButton("Стоп ❌")
    stop_markup.add(stop_button)

    return stop_markup

def create_group_markup() -> ReplyKeyboardMarkup:
    """Fucntion that will create ReplyKeyboard for admins to mention anyone anytime

    Returns:
        ReplyKeyboardMarkup: created markup for unlogged user command
    """
    group_markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    everyone_button = KeyboardButton("@all 📢")
    forest_button = KeyboardButton("Лесной союз 🍃")
    magic_button = KeyboardButton("Магический совет 🔮")
    light_button = KeyboardButton("Королевство света ☀️")
    tech_button = KeyboardButton("Техногенное общество 💡")
    dark_button = KeyboardButton("Тёмные владения 🦇")

    group_markup.add(
        everyone_button, 
        forest_button, 
        magic_button, 
        light_button, 
        tech_button, 
        dark_button
    )

    return group_markup

def create_unlogged_markup() -> ReplyKeyboardMarkup:
    """Fucntion that will create ReplyKeyboard for unlogged user and return it

    Returns:
        ReplyKeyboardMarkup: created markup for unlogged user command
    """
    unlogged_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = KeyboardButton("Начать ⭐")
    unlogged_markup.add(start_button)

    return unlogged_markup