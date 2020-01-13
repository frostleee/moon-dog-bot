import requests
import re
import datetime
import random

from bs4 import BeautifulSoup
from cachetools import cached, TTLCache
from telegram.ext import Updater, CallbackContext
from telegram.parsemode import ParseMode
from utils.exceptions import GoroskopException
from handlers.commands import command

zodiac_signs = [
    'Овен', 'Телец', 'Близнецы', 'Рак',
    'Лев', 'Дева', 'Весы', 'Скорпион',
    'Стрелец', 'Козерог', 'Водолей', 'Рыбы'
]

advice = [
    '*Межгалактический совет*', '*Лунный совет*',
    '*Собачий совет*', '*Совет от первого ордена*',
    '*Совет*'
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

        ad = goroskop_list[zodiac]['advice'].replace('Космический совет', random.choice(advice))
        text = goroskop_list[zodiac]['text']
        message = '*%s*:\n%s\n%s' % (zodiac, text, ad)

        context.bot.send_message(chat_id=chat_id,
                                 text=message,
                                 parse_mode=ParseMode.MARKDOWN)
    except GoroskopException as e:
        updater.message.reply_text(text=str(e), parse_mode=ParseMode.MARKDOWN)


@cached(cache=TTLCache(maxsize=1024, ttl=7200))
def get_goroskop():
    goroskop_url = get_everyday_url()

    if not goroskop_url:
        raise GoroskopException('Чет астрологи мне наговорили всякой херни, ничего не понял')

    soup = get_beautiful_soup(goroskop_url)

    goroskop = dict()

    for zodiac in zodiac_signs:
        regex = r'(.*)?(' + re.escape(zodiac) + r')$'
        p = soup.find(name=re.compile('p|h3'), text=re.compile(regex))
        text = p.find_next('p')
        advice = text.find_next('p')
        goroskop[zodiac] = {
            'text': text.text,
            'advice': advice.text
        }

    return goroskop


@cached(cache=TTLCache(maxsize=256, ttl=72000))
def get_everyday_url():
    soup = get_beautiful_soup('https://www.5-tv.ru/news/goroskop/')
    last_posts = soup.find(name='div', attrs={'class': ['col8', 'col4']})
    links = last_posts.find_all_next(name='a')

    regex = r'(.*)?((Гороскоп).*%d(.*)(\d{4})?)(.*)?' % datetime.datetime.now().day
    result_link = None

    for link in links:
        h3 = link.find_next(name='h3', attrs={'class': 'link'}, text=re.compile(regex))
        if h3:
            result_link = link.get('href')
        else:
            fs_text = link.find_next(name='p', attrs={'class': 'fsText'})
            strong = fs_text.find_next(name='strong', attrs={'class': 'link'}, text=re.compile(regex))
            if strong:
                result_link = link.get('href')

        if result_link:
            break

    return result_link


def get_beautiful_soup(url: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0'
    }

    r = requests.get(url=url, headers=headers)

    if int(r.status_code) != 200:
        raise GoroskopException('Не смог достучаться до астрологов, сорри :(')

    return BeautifulSoup(r.content, 'html.parser')
