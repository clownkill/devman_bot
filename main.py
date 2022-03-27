import os
from pprint import pprint

import requests
from dotenv import load_dotenv

load_dotenv()

devman_token = os.getenv('DEVMAN_TOKEN')

user_reviews_url = 'https://dvmn.org/api/user_reviews/'

headers = {
    'Authorization': f'Token {devman_token}',
}

response = requests.get(user_reviews_url, headers=headers)
response.raise_for_status()

pprint(response.text)