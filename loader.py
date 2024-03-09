import os

from dotenv import load_dotenv
from telebot import TeleBot

from database.dbworker import create_db_engine

load_dotenv("config.env")
TOKEN = os.environ.get('BOT_TOKEN')
dev_id = os.environ.get('DEV_ID')
leader_id = os.environ.get('LEADER_ID')
secret_word = os.environ.get('AUTH_WORD')
engine = create_db_engine()
bot = TeleBot(TOKEN)
