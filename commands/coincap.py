import requests
import telegram

from telegram.ext import Updater, CallbackContext
from utils.messages import RandomFunMessages
from .decorator import command

url = 'https://api.coincap.io/v2/assets?limit=20'

symbols = {
    'биток': 'BTC',
    'эфир': 'ETH'
}


@command.register(name='крипта')
def coincap(updater: Updater, context: CallbackContext, args: list):
    response = requests.get(url)

    if int(response.status_code) == 200:
        message = 'Курс всех популярных валют:\n'
        chat_id = updater.message.chat_id
        json = response.json()
        coincaps = json['data']
        if args:
            try:
                message = get_message_by_arg(args[0], coincaps)
            except ValueError as e:
                message = RandomFunMessages.get('error')
        else:
            for coincap in coincaps:
                message += '%s - *%f* (%f)\n' % (coincap['symbol'],
                                                 float(coincap['priceUsd']),
                                                 float(coincap['changePercent24Hr']))

        context.bot.send_message(chat_id=chat_id, text=message, parse_mode=telegram.ParseMode.MARKDOWN)


def get_message_by_arg(arg=None, data=None):
    if arg not in symbols:
        raise ValueError('undefined symbol')
    symbol = symbols[arg]
    coincap = get_coincap_by_symbol(symbol, data)
    return '%s сейчас стоит *%f* (%f)' % (symbol, float(coincap['priceUsd']), float(coincap['changePercent24Hr']))


def get_coincap_by_symbol(id: str, data: list):
    find = next(filter(lambda x: x['symbol'] == id, data))
    if find:
        return find
    return None
