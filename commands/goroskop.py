import requests
import re
from bs4 import BeautifulSoup
from cachetools import cached, TTLCache
from telegram.ext import Updater, CallbackContext
from telegram.parsemode import ParseMode

from utils.exceptions import GoroskopException
from utils.messages import RandomFunMessages
from .decorator import command

url = 'https://www.5-tv.ru/news/goroskop/'

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0'
}

zodiac_signs = [
    'Овен', 'Телец', 'Близнецы', 'Рак',
    'Лев', 'Дева', 'Весы', 'Скорпион',
    'Стрелец', 'Козерог', 'Водолей', 'Рыбы'
]


@command.register(name='гороскоп')
def goroskop(updater: Updater, context: CallbackContext, args: list):
    try:
        if not args:
            raise GoroskopException(
                'Выбери один из знаков зодиака:\n%s\n*Пример:* гороскоп рыбы' % ', '.join(zodiac_signs))

        zodiac = args[0].title()
        if zodiac not in zodiac_signs:
            raise GoroskopException('Мне не известен этот знак зодиака')

        chat_id = updater.message.chat_id
        goroskop_list = get_goroskop(chat_id, context)
        text = '*%s*:\n%s' % (zodiac, goroskop_list[zodiac])
        context.bot.send_message(chat_id=chat_id,
                                 text=text,
                                 parse_mode=ParseMode.MARKDOWN)
    except GoroskopException as e:
        updater.message.reply_text(text=str(e), parse_mode=ParseMode.MARKDOWN)


@cached(TTLCache(maxsize=2048, ttl=7200))
def get_goroskop(chat_id, context: CallbackContext):
    context.bot.send_message(chat_id=chat_id, text=RandomFunMessages.get('goroskop'))
    goroskop_url = get_everyday_url()
    r = requests.get(goroskop_url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    goroskop = dict()
    for zodiac in zodiac_signs:
        regex = r'(.*)?(' + re.escape(zodiac) + r')$'
        p = soup.find(name=re.compile('p|h3'), text=re.compile(regex))
        goroskop[zodiac] = p.find_next('p').text
    return goroskop


def get_everyday_url():
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise GoroskopException('Не смог достучаться до астрологов, сорри :(')
    soup = BeautifulSoup(r.content, 'html.parser')
    container = soup.find('div', {'class': 'col8'})
    return container.a.get('href')
