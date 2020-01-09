import logging

from telegram.ext import Updater, CallbackContext


class Commands:
    def __init__(self):
        self.__handlers = {}
        self.__descriptions = {}

    def call(self, updater: Updater, context: CallbackContext):
        args = updater.message.text.split(' ')
        if args[2] and args[2] in self.__handlers:
            f = self.__handlers[args[2]]
            if callable(f):
                f(updater=updater, context=context, args=args[3:])

    def register(self, name: str, description=None):
        self.__descriptions[name] = description

        def handler(f):
            commands = name.split('|')
            for cmd in commands:
                if cmd not in self.__handlers:
                    self.__handlers[cmd] = f
            return f

        return handler

    def get_descriptions(self):
        return self.__descriptions


command = Commands()
