import os
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
            lessons_review = response.json()
            if lessons_review['status'] == 'timeout':
                params['timestamp'] = lessons_review['timestamp_to_request']
            else:
                last_checking_attempt = lessons_review['new_attempts'][0]
                params['timestamp'] = lessons_review['last_attempt_timestamp']

                send_checking_result(
                    telegram_bot=telegram_bot,
                    telegram_chat_id=telegram_chat_id,
                    last_checking_attempt=last_checking_attempt
                )
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            sleep(time_to_sleep)


def main():
    load_dotenv()

    devman_token = os.environ['DEVMAN_TOKEN']
    telegram_token = os.environ['TELEGRAM_TOKEN']
    telegram_chat_id = os.environ['TELEGRAM_CHAT_ID']

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
