import logging
import os
from textwrap import dedent
from time import sleep

import requests
import telegram
from dotenv import load_dotenv


class TelegramLogsHandler(logging.Handler):

    def __init__(self, bot, telegram_chat_id):
        super().__init__()
        self.telegram_chat_id = telegram_chat_id
        self.bot = bot

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(
            chat_id=self.telegram_chat_id,
            text=log_entry
        )


def send_checking_result(telegram_bot, telegram_chat_id, last_checking_attempt):
    lesson_title = last_checking_attempt['lesson_title']
    lesson_url = last_checking_attempt['lesson_url']

    if not last_checking_attempt['is_negative']:
        message_text = f'''
        У вас проверили работу "{lesson_title}".
        
        Преподователю все понравилось, можно приступать к следующему уроку!
        
        {lesson_url}
        '''
        telegram_bot.send_message(
            text=dedent(message_text),
            chat_id=telegram_chat_id
        )
    else:
        message_text = f'''
        У вас проверили работу "{lesson_title}"

        К сожалению в работе нашлись ошибки.

        {lesson_url}
        '''
        telegram_bot.send_message(
            text=dedent(message_text),
            chat_id=telegram_chat_id
        )


def check_devman_lesson_result(devman_token, telegram_bot, telegram_chat_id, time_to_sleep=60):
    long_polling_url = 'https://dvmn.org/api/long_polling/'
    headers = {
        'Authorization': f'Token {devman_token}',
    }
    params = {}

    while True:
        try:
            0/0
        except requests.exceptions.ReadTimeout:
            logging.warning('Нет ответа от сервера')
            continue
        except requests.exceptions.ConnectionError:
            logging.warning('Проблемы с подключением к интернету')
            sleep(time_to_sleep)
        except Exception as err:
            logging.error(err, exc_info=True)


def main():
    load_dotenv()

    devman_token = os.environ['DEVMAN_TOKEN']
    telegram_token = os.environ['TELEGRAM_TOKEN']
    telegram_chat_id = os.environ['TELEGRAM_CHAT_ID']

    bot = telegram.Bot(telegram_token)

    time_to_sleep = 60

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(bot, telegram_chat_id))

    check_devman_lesson_result(
        devman_token=devman_token,
        telegram_bot=bot,
        telegram_chat_id=telegram_chat_id,
        time_to_sleep=time_to_sleep
    )


if __name__ == '__main__':
    main()
