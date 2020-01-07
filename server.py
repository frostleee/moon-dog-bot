import logging

from telegram.ext import Updater, CallbackContext, MessageHandler, Filters, Dispatcher
from utils.settings import get
from commands.decorator import command

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    request_kwargs = None
    token = get('app_token')

    if bool(get('app_use_proxy')):
        request_kwargs = {
            'proxy_url': get('app_proxy_url')
        }

    updater = Updater(token=token, request_kwargs=request_kwargs, use_context=True)
    dispatcher = updater.dispatcher

    init_dispatcher_handlers(dispatcher)

    updater.start_polling()
    updater.idle()


def init_dispatcher_handlers(dispatcher: Dispatcher):
    dispatcher.add_handler(MessageHandler(filters=Filters.regex(r'^(Л|л)унный п(е|ё)с'),
                                          callback=command.call))


def error(updater: Updater, context: CallbackContext):
    logger.warning('Error: %s - Updater: %s', context, updater)


if __name__ == '__main__':
    main()
