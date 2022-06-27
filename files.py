import requests
import sys
from config import token


class sBot:
    def __init__(self, TOKEN, CHAT_ID):
        self.token = TOKEN
        self.chat_id = CHAT_ID

    def send_file(self, files=None):
        url = f'https://api.telegram.org/bot{self.token}/sendDocument'
        requests.post(url=url, data={"chat_id": self.chat_id}, files=files)


def file_xlsx():
    with open(f"reports/{file_name}.xlsx", mode='rb') as filexlsx:
        bot.send_file(files={"document": filexlsx})


def file_log():
    with open(f"log/{file_name}.log", mode='rb') as filexlsx:
        bot.send_file(files={"document": filexlsx})


if __name__ == '__main__':
    file_name = sys.argv[1]
    type_file = sys.argv[2]
    chat_id = sys.argv[3]
    bot = sBot(token, chat_id)
    if type_file == 'xlsx':
        file_xlsx()
    elif type_file == 'log':
        file_log()
