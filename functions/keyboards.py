from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
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
    edit_button = KeyboardButton("Изменить профиль ✏️")
    help_button = KeyboardButton("Помощь 📃")

    if (not user_id in DEVS) and (not user_id in ADMINS):
        start_markup.add(profile_button, edit_button, help_button)
    else:
        start_markup.add(
            all_button, new_button, del_button, view_button, profile_button, edit_button, help_button
        )

    return start_markup


def create_edit_markup() -> ReplyKeyboardMarkup:
    """Fucntion that will create ReplyKeyboard for "/edit" command and return it

    Returns:
        ReplyKeyboardMarkup: created markup for "/edit" command
    """
    edit_markup = ReplyKeyboardMarkup(resize_keyboard=True)

    gamename_button = KeyboardButton("Никнейм 🪪")
    crit_button = KeyboardButton("Крит. урон 🔪")
    uid_button = KeyboardButton("UID 📄")
    fractions_button = KeyboardButton("Фракции в драконе 🔮")
    platfrom_button = KeyboardButton("Платформа 📱")
    pawns_button = KeyboardButton("Особые пешки 🎉")
    nothing_button = KeyboardButton("Ничего ❌")

    edit_markup.add(
        gamename_button,
        crit_button,
        uid_button,
        fractions_button,
        platfrom_button,
        pawns_button,
        nothing_button
    )

    return edit_markup


def create_all_markup(templates_amt: int) -> ReplyKeyboardMarkup:
    """Fucntion that will create ReplyKeyboard for "/all" command and return it

    Args:
        templates_amt (int): amount of stored templates in database

    Returns:
        ReplyKeyboardMarkup: created markup for "/all" command
    """
    all_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    all_buttons = []

    for button in range(templates_amt):
        markup_button = KeyboardButton(f"{button+1} 💾")
        all_buttons.append(markup_button)

    all_markup.add(*all_buttons)
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
    all_buttons = []

    for button in range(templates_amt):
        markup_button = KeyboardButton(f"{button+1} 💾")
        all_buttons.append(markup_button)

    view_markup.add(*all_buttons)
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
    all_buttons = []

    for button in range(templates_amt):
        markup_button = KeyboardButton(f"{button+1} 💾")
        all_buttons.append(markup_button)

    del_markup.add(*all_buttons)
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
    banshee_button = KeyboardButton("Банши 😈")
    tesla_button = KeyboardButton("Тесла ⚡️")
    robot_button = KeyboardButton("Робот 🤖")
    panda_button = KeyboardButton("Панда 🐼")

    group_markup.add(
        everyone_button, 
        forest_button, 
        magic_button, 
        light_button, 
        tech_button, 
        dark_button,
        banshee_button,
        tesla_button,
        robot_button,
        panda_button
    )

    return group_markup


def create_welcome_markup() -> ReplyKeyboardMarkup:
    """Function that creates welcome markup and return it

    Returns:
        ReplyKeyboardMarkup: markup to apply for a clan or to register
    """
    welcome_markup = ReplyKeyboardMarkup(resize_keyboard=True)

    reg_button = KeyboardButton("Уже участник 🔍")
    apply_button = KeyboardButton("Подать заявку 📨")
    stop_button = KeyboardButton("Стоп ❌")

    welcome_markup.add(reg_button, apply_button)
    welcome_markup.add(stop_button)

    return welcome_markup


def create_requirements_markup() -> ReplyKeyboardMarkup:
    """Function that creates requirements markup and return it

    Returns:
        ReplyKeyboardMarkup: markup to accept or to deny requirements
    """
    requirements_markup = ReplyKeyboardMarkup(resize_keyboard=True)

    accept_button = KeyboardButton("Согласен ✅")
    deny_button = KeyboardButton("Не согласен ❌")
    stop_button = KeyboardButton("Стоп ❌")

    requirements_markup.add(accept_button, deny_button)
    requirements_markup.add(stop_button)

    return requirements_markup


def create_check_markup() -> ReplyKeyboardMarkup:
    """Function that creates appliance markup and return it

    Returns:
        ReplyKeyboardMarkup: markup to accept or to deny correctness of appliance
    """
    check_markup = ReplyKeyboardMarkup(resize_keyboard=True)

    accept_button = KeyboardButton("Верно ✅")
    deny_button = KeyboardButton("Не верно ❌")
    stop_button = KeyboardButton("Стоп ❌")

    check_markup.add(accept_button, deny_button)
    check_markup.add(stop_button)

    return check_markup


def create_unlogged_markup() -> ReplyKeyboardMarkup:
    """Fucntion that will create ReplyKeyboard for unlogged user and return it

    Returns:
        ReplyKeyboardMarkup: created markup for unlogged user command
    """
    unlogged_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = KeyboardButton("Начать ⭐")
    unlogged_markup.add(start_button)

    return unlogged_markup


def create_accept_markup(user_id: int) -> InlineKeyboardMarkup:
    """Function that creates inline keyboard for admins to accept or deny an appliance

    Args:
        user_id (int): user's id that is defined by Telegram

    Returns:
        InlineKeyboardMarkup: created inline markup for admins
    """
    accept_markup = InlineKeyboardMarkup()

    accept_button = InlineKeyboardButton("Принять ✅", callback_data=("a"+str(user_id)))
    deny_button = InlineKeyboardButton("Отклонить ❌", callback_data=("d"+str(user_id)))

    accept_markup.add(accept_button, deny_button)

    return accept_markup