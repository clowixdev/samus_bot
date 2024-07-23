from loader import bot, media_groups, DEVS, ADMINS
from telebot.types import Message

@bot.message_handler(content_types=["photo"])
def gather_all_photos_in_media_group(message: Message) -> None:

    if message.from_user.id != message.chat.id:
        return

    if message.from_user.id not in media_groups:
        return

    photo_info = bot.get_file(message.photo[-1].file_id)
    photo_bytes = bot.download_file(photo_info.file_path)
    media_groups[message.from_user.id] += [photo_bytes]