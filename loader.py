import os

from dotenv import load_dotenv
from telebot import TeleBot

from database.dbworker import create_db_engine

load_dotenv("config.env")
TOKEN = os.environ.get('BOT_TOKEN')
dev_id = os.environ.get('DEV_ID')
engine = create_db_engine()
bot = TeleBot(TOKEN)
