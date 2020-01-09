from telegram.ext import Updater, CallbackContext
from telegram.parsemode import ParseMode

from .decorator import command


@command.register(name='помощь', description='список всех собачьих комманд')
def help(updater: Updater, context: CallbackContext, args: list):
    message = 'Список комманд которым я слушаюсь\n'
    for k, v in command.get_descriptions().items():
        message += '*' + k.replace('|', '* или *') + '*'
        if not v:
            message += ' - хрен знает что оно делает'
        else:
            message += ' - ' + v
        message += '\n'

    chat_id = updater.message.chat_id
    context.bot.send_message(chat_id=chat_id, text=message, parse_mode=ParseMode.MARKDOWN)
