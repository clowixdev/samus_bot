import os

from dotenv import load_dotenv
from telebot import TeleBot, ExceptionHandler

from database.dbworker import create_db_engine, load_blacklist

from datetime import datetime

load_dotenv("tokens.env")
TOKEN = os.environ.get("BOT_TOKEN")

dev_id = os.environ.get("DEV_ID")
leader_id = os.environ.get("LEADER_ID")
fhelper_id = os.environ.get("FHELPER_ID")
fofficer_id = os.environ.get("FOFFICER_ID")
sofficer_id = os.environ.get("SOFFICER_ID")
tofficer_id = os.environ.get("TOFFICER_ID")
frofficer_id = os.environ.get("FROFFICER_ID")
sxofficer_id = os.environ.get("SXOFFICER_ID")
seventh_off_id = os.environ.get("SEVENTH_OFF_ID")

main_chat_id = os.environ.get("MAIN_CHAT_ID")
admins_chat_id = os.environ.get("ADMINS_CHAT_ID")
general_chat_link = os.environ.get("MAIN_CHAT_LINK")

DEVS = [int(dev_id)]
ADMINS = [
    int(leader_id), int(fhelper_id), 
    int(fofficer_id), int(sofficer_id), 
    int(tofficer_id), int(frofficer_id),
    int(sxofficer_id), int(seventh_off_id)
    ]

last_message = dict()
current_polls = dict()
userdata = dict()
appliances = dict()
media_groups = dict()
polls = dict()

class CloExceptionHandler(ExceptionHandler):
    """Handler that will be called if any exception is called during polling

    Args:
        ExceptionHandler (class): Base class from telebot
    """ 
    def handle(self, exception) -> bool:
        print("EXC.:", datetime.now(), exception)

        return True

secret_word = os.environ.get("AUTH_WORD")
engine = create_db_engine()
blacklist = load_blacklist()
bot = TeleBot(TOKEN, exception_handler=CloExceptionHandler())