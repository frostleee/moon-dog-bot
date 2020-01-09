import requests
import random
import re

from telegram.ext import Updater, CallbackContext
from handlers.commands import command


@command.register(name='dankmemes', description='выводит случайный мем из r/dankmemes/hot')
def dankmemes(updater: Updater, context: CallbackContext, args: list):
    send_image(context=context,
               chat_id=int(updater.message.chat_id),
               url='https://www.reddit.com/r/dankmemes/hot.json?limit=100')


@command.register(name='memes|мем', description='выводит случайный мем из r/memes/hot')
def memes(updater: Updater, context: CallbackContext, args: list):
    send_image(context=context,
               chat_id=int(updater.message.chat_id),
               url='https://www.reddit.com/r/memes/hot.json?limit=100')


def send_image(context: CallbackContext, chat_id: int, url: str):
    mem = get_random_post(url)
    if mem:
        data = mem['data']
        media_url = data['url']
        context.bot.send_photo(chat_id=chat_id, photo=media_url)


def get_random_post(url: str):
    def get_post(posts_list: list):
        post = random.choice(posts_list)
        media_url = post['data']['url']
        if media_url and re.match(r'(.*).(jpg|jpeg|png)', media_url):
            return post
        return get_post(posts_list)

    result = None
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0'
    }
    response = requests.get(url=url, headers=headers)
    if int(response.status_code) == 200:
        json = response.json()
        data = json['data']['children']
        result = get_post(data)
    return result
