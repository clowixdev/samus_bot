import os

from dotenv import load_dotenv
from telebot import TeleBot

from database.dbworker import create_db_engine

load_dotenv("config.env")
TOKEN = os.environ.get("BOT_TOKEN")

dev_id = os.environ.get("DEV_ID")
leader_id = os.environ.get("LEADER_ID")

DEVS = [int(dev_id)]
ADMINS = [int(leader_id)]

main_chat = os.environ.get("MAIN_CHAT_ID")
dragon_chat  = os.environ.get("DRAGON_CHAT_ID")

CHATS = [int(main_chat), int(dragon_chat)]

secret_word = os.environ.get("AUTH_WORD")
engine = create_db_engine()
bot = TeleBot(TOKEN)
