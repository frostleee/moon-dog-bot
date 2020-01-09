import sqlite3
import utils.settings as settings
from telegram.ext import Updater, CallbackContext


class Database:
    def __init__(self):
        self.__database = str(settings.get('app_database'))

    def use(self):
        def handler(f):
            def wrapper(updater: Updater, context: CallbackContext, args: list):
                connection = sqlite3.connect(self.__database)
                cursor = connection.cursor()
                result = f(updater=updater,
                           context=context,
                           args=args,
                           connection=connection,
                           cursor=cursor)
                cursor.close()
                return result

            return wrapper

        return handler


db = Database()
