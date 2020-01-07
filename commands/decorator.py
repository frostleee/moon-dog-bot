from telegram.ext import Updater, CallbackContext


class Commands:
    def __init__(self):
        self.handlers = {}

    def call(self, updater: Updater, context: CallbackContext):
        args = updater.message.text.split(' ')
        if args[2] and args[2] in self.handlers:
            f = self.handlers[args[2]]
            if callable(f):
                f(updater=updater, context=context, args=args[3:])

    def register(self, name: str):
        def handler(f):
            commands = name.split('|')
            for cmd in commands:
                if cmd not in self.handlers:
                    self.handlers[cmd] = f
            return f

        return handler


command = Commands()
