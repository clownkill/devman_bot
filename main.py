import os
from pprint import pprint

import requests
import telegram
from dotenv import load_dotenv


def main():
    load_dotenv()

    devman_token = os.getenv('DEVMAN_TOKEN')
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('CHAT_ID')

    long_polling_url = 'https://dvmn.org/api/long_polling/'
    headers = {
        'Authorization': f'Token {devman_token}',
    }
    params = {}

    while True:
        try:
            response = requests.get(long_polling_url, params=params, headers=headers)
            response.raise_for_status()
            dvmn_response_json = response.json()
            if dvmn_response_json['status'] != 'timeout':
                params['timestamp'] = response.json()['new_attempts'][0]['timestamp']
            else:
                continue
        except requests.exceptions.ReadTimeout:
            print('Нет ответа от сервера')
            continue
        except requests.exceptions.ConnectionError:
            print('Отсутствует подключение к интернету')
            continue

        bot = telegram.Bot(token=telegram_token)

        lesson_title = dvmn_response_json['new_attempts'][0]['lesson_title']
        lesson_url = dvmn_response_json['new_attempts'][0]['lesson_url']

        if not dvmn_response_json['new_attempts'][0]['is_negative']:
            bot.send_message(
                text=f'У вас проверили работу "{lesson_title}". \n\n'
                     f'Преподователю все понравилось, можно приступать к следующему уроку!'
                     f'Ссылка на урок: {lesson_url}',
                chat_id=chat_id
            )
        else:
            bot.send_message(
                text=f'У вас проверили работу "{lesson_title}".\n\n'
                     f'К сожалению в работе нашлись ошибки.\n\n'
                     f'{lesson_url}',
                chat_id=chat_id
            )

        pprint(response.json())


if __name__ == '__main__':
    main()
