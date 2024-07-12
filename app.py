from loader import bot
from telebot import apihelper
from time import sleep
from datetime import datetime
from requests.exceptions import ConnectionError, ReadTimeout
from sys import exit
import commands

if __name__ == "__main__":
    while True:
        try:
            print(f"START: {datetime.now()} Bot script has been successfully enabled")
            bot.polling(non_stop=True, interval=0)
        except apihelper.ApiTelegramException as tele_e:
            print("EXCEPTION:", datetime.now(), tele_e)
            sleep(4)
            continue
        except (ConnectionError, ReadTimeout) as req_e:
            print("EXCEPTION:", datetime.now(), req_e)
            sleep(4)
            continue
