from loader import bot
from time import sleep
from datetime import datetime
from requests.exceptions import ConnectionError, ReadTimeout
from sys import exit
import commands

if __name__ == "__main__":
    while True:
        try:
            print(f"Bot script has been successfully enabled at {datetime.now()}")
            bot.polling(non_stop=True, interval=0)
        except KeyboardInterrupt:
            print(f"Shutting down the bot at {datetime.now()}")
            exit(0)
        except (ConnectionError, ReadTimeout) as r_e:
            print(datetime.now(), r_e)
            sleep(5)
            continue
