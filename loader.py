import os

from dotenv import load_dotenv
from telebot import TeleBot

from database.dbworker import create_db_engine

load_dotenv("config.env")
TOKEN = os.environ.get("BOT_TOKEN")

dev_id = os.environ.get("DEV_ID")
leader_id = os.environ.get("LEADER_ID")
fhelper_id = os.environ.get("FHELPER_ID")
fofficer_id = os.environ.get("FOFFICER_ID")
sofficer_id = os.environ.get("SOFFICER_ID")
tofficer_id = os.environ.get("TOFFICER_ID")

DEVS = [int(dev_id)]
ADMINS = [int(leader_id), int(fhelper_id), int(fofficer_id), int(sofficer_id), int(tofficer_id)]

main_chat = os.environ.get("MAIN_CHAT_ID")

CHATS = [int(main_chat)]

last_message = dict()
current_polls = ""

secret_word = os.environ.get("AUTH_WORD")
engine = create_db_engine()
bot = TeleBot(TOKEN)
