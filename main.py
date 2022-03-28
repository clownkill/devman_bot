import os

import requests
import telegram
from dotenv import load_dotenv


def send_checking_result(telegram_token, telegram_chat_id, devman_information_from_api):
    bot = telegram.Bot(token=telegram_token)

    lesson_title = devman_information_from_api['new_attempts'][0]['lesson_title']
    lesson_url = devman_information_from_api['new_attempts'][0]['lesson_url']

    if not devman_information_from_api['new_attempts'][0]['is_negative']:
        bot.send_message(
            text=f'У вас проверили работу "{lesson_title}". \n\n'
                 f'Преподователю все понравилось, можно приступать к следующему уроку!'
                 f'Ссылка на урок: {lesson_url}',
            chat_id=telegram_chat_id
        )
    else:
        bot.send_message(
            text=f'У вас проверили работу "{lesson_title}".\n\n'
                 f'К сожалению в работе нашлись ошибки.\n\n'
                 f'{lesson_url}',
            chat_id=telegram_chat_id
        )


def check_devman_lesson_result(devman_token, telegram_token, telegram_chat_id):
    long_polling_url = 'https://dvmn.org/api/long_polling/'
    headers = {
        'Authorization': f'Token {devman_token}',
    }
    params = {}

    while True:
        try:
            response = requests.get(long_polling_url, params=params, headers=headers)
            response.raise_for_status()
            devman_information_from_api = response.json()
            if devman_information_from_api['status'] != 'timeout':
                params['timestamp'] = devman_information_from_api['new_attempts'][0]['timestamp']
            else:
                continue
        except requests.exceptions.ReadTimeout:
            print('Нет ответа от сервера')
            continue
        except requests.exceptions.ConnectionError:
            print('Отсутствует подключение к интернету')
            continue

        send_checking_result(
            telegram_token=telegram_token,
            telegram_chat_id=telegram_chat_id,
            devman_information_from_api=devman_information_from_api
        )


def main():
    load_dotenv()

    devman_token = os.getenv('DEVMAN_TOKEN')
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

    check_devman_lesson_result(
        devman_token=devman_token,
        telegram_token=telegram_token,
        telegram_chat_id=telegram_chat_id
    )


if __name__ == '__main__':
    main()
