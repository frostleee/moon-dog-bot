import requests
import re
import datetime
import sys

from bs4 import BeautifulSoup
from cachetools import cached, TTLCache
from telegram.ext import Updater, CallbackContext
from telegram.parsemode import ParseMode
from utils.exceptions import GoroskopException
from handlers.commands import command

url = 'https://www.5-tv.ru/news/goroskop/'

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0'
}

zodiac_signs = [
    'Овен', 'Телец', 'Близнецы', 'Рак',
    'Лев', 'Дева', 'Весы', 'Скорпион',
    'Стрелец', 'Козерог', 'Водолей', 'Рыбы'
]


@command.register(name='гороскоп', description='скажет что говорят звезды на сегоднящний день')
def goroskop(updater: Updater, context: CallbackContext, args: list):
    try:
        if not args:
            raise GoroskopException(
                'Выбери один из знаков зодиака:\n%s\n*Пример:* гороскоп рыбы' % ', '.join(zodiac_signs))

        zodiac = args[0].title()
        if zodiac not in zodiac_signs:
            raise GoroskopException('Мне не известен этот знак зодиака')

        chat_id = updater.message.chat_id
        goroskop_list = get_goroskop()
        text = '*%s*:\n%s' % (zodiac, goroskop_list[zodiac])
        context.bot.send_message(chat_id=chat_id,
                                 text=text,
                                 parse_mode=ParseMode.MARKDOWN)
    except GoroskopException as e:
        updater.message.reply_text(text=str(e), parse_mode=ParseMode.MARKDOWN)


@cached(cache=TTLCache(maxsize=1024, ttl=7200))
def get_goroskop():
    goroskop_url = get_everyday_url()

    if not goroskop_url:
        raise GoroskopException('Не смог достучаться до астрологов, сорри :('
                                '')
    r = requests.get(goroskop_url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    goroskop = dict()

    for zodiac in zodiac_signs:
        regex = r'(.*)?(' + re.escape(zodiac) + r')$'
        p = soup.find(name=re.compile('p|h3'), text=re.compile(regex))
        goroskop[zodiac] = p.find_next('p').text

    return goroskop


@cached(cache=TTLCache(maxsize=256, ttl=72000))
def get_everyday_url():
    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        raise GoroskopException('Не смог достучаться до астрологов, сорри :(')

    now = datetime.datetime.now()
    regex = r'(.*)?((Гороскоп).*%d(.*)\d{4})(.*)?' % now.day
    soup = BeautifulSoup(r.content, 'html.parser')
    last_posts = soup.find(name='div', attrs={'class': 'col4'})
    links = last_posts.find_all_next(name='a')

    for link in links:
        fs_text = link.find_next(name='p', attrs={'class': 'fsText'})
        strong = fs_text.find_next(name='strong', attrs={'class': 'link'}, text=re.compile(regex))
        if strong:
            return link.get('href')

    return None
