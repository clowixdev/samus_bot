from loader import bot, media_groups
from telebot.types import Message

@bot.message_handler(content_types=["photo"])
def gather_all_photos_in_media_group(message: Message) -> None:
    """This handler will gather all the photos that are send in media groups 
    and sort them by user_id that is defined by telegram. 

    Args:
        message (Message): Object, that contains information of received message
    """

    if message.from_user.id != message.chat.id:
        return

    if message.from_user.id not in media_groups:
        return

    photo_info = bot.get_file(message.photo[-1].file_id)
    photo_bytes = bot.download_file(photo_info.file_path)
    media_groups[message.from_user.id] += [photo_bytes]