import os
from datetime import datetime as dt
from textwrap import dedent
from time import sleep

import requests
import telegram
from dotenv import load_dotenv


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
            response = requests.get(long_polling_url, params=params, headers=headers)
            response.raise_for_status()
            decoded_response = response.json()
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            sleep(time_to_sleep)

        if decoded_response['status'] == 'timeout':
            params['timestamp'] = decoded_response['timestamp_to_request']
        else:
            last_checking_attempt = decoded_response['new_attempts'][0]
            params['timestamp'] = dt.timestamp(dt.now())

            send_checking_result(
                telegram_bot=telegram_bot,
                telegram_chat_id=telegram_chat_id,
                last_checking_attempt=last_checking_attempt
            )


def main():
    load_dotenv()

    devman_token = os.getenv('DEVMAN_TOKEN')
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

    bot = telegram.Bot(telegram_token)

    time_to_sleep = 60

    check_devman_lesson_result(
        devman_token=devman_token,
        telegram_bot=bot,
        telegram_chat_id=telegram_chat_id,
        time_to_sleep=time_to_sleep
    )


if __name__ == '__main__':
    main()
