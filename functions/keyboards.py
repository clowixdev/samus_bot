from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

def create_start_markup() -> ReplyKeyboardMarkup:
    """Fucntion that will create ReplyKeyboard for "/start" command and return it

    Returns:
        ReplyKeyboardMarkup: created markup for "/start" command
    """
    start_markup = ReplyKeyboardMarkup(resize_keyboard=True)

    all_button = KeyboardButton("Рассылка клану 📨")
    new_button = KeyboardButton("Создать шаблон 📝")
    del_button = KeyboardButton("Удалить шаблон 🧹")
    help_button = KeyboardButton("Помощь 📃")

    start_markup.add(all_button, new_button, del_button, help_button)

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

    new_button = KeyboardButton("Создать шаблон 📝")
    instant_send_button = KeyboardButton("Отправить без сохранения 📋")

    all_markup.add(new_button, instant_send_button)

    return all_markup

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
    help_button = KeyboardButton("Помощь 📃")
    help_markup.add(help_button)

    return help_markup