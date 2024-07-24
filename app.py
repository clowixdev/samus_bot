from loader import bot
from telebot.apihelper import ApiException, ApiTelegramException
from time import sleep
from datetime import datetime
from requests.exceptions import ConnectionError, ReadTimeout
import commands

if __name__ == "__main__":
    while True:
        try:
            print(f"START: {datetime.now()} Bot script has been successfully enabled")
            bot.polling(non_stop=True, interval=0)
        except (ApiTelegramException, ApiException) as tele_e:
            print("EXCEPTION (TELEGRAM):", datetime.now(), tele_e)
            sleep(3)
            continue
        except (ConnectionError, ReadTimeout) as req_e:
            print("EXCEPTION: (TIMEOUT)", datetime.now(), req_e)
            sleep(3)
            continue
