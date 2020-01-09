import requests
import random
import re

from telegram.ext import Updater, CallbackContext
from .decorator import command

url = 'https://www.reddit.com/r/dankmemes/new.json?limit=100'

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0'
}


@command.register(name='dankmemes', description='выводит случайный мем из r/dankmemes')
def dankmemes(updater: Updater, context: CallbackContext, args: list):
    response = requests.get(url=url, headers=headers)

    if int(response.status_code) == 200:
        json = response.json()
        data = json['data']['children']
        context.bot.send_photo(chat_id=updater.message.chat_id,
                               photo=get_random_memes(data))


def get_random_memes(data):
    random_data = random.choice(data)
    url = random_data['data']['url']
    if url and re.match(r'(.*).(jpg|jpeg|png)', url):
        return url

    return get_random_memes(data)
