import os
from pprint import pprint

import requests
from dotenv import load_dotenv

load_dotenv()

devman_token = os.getenv('DEVMAN_TOKEN')

user_reviews_url = 'https://dvmn.org/api/user_reviews/'
long_polling_url = 'https://dvmn.org/api/long_polling/'

headers = {
    'Authorization': f'Token {devman_token}',
}

while True:
    response = requests.get(long_polling_url, headers=headers)
    response.raise_for_status()

    pprint(response.json())