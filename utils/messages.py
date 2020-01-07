import random


class RandomFunMessages:
    messages = {
        'error': [
            'Может ты нахуй пойдешь с такими запросами?',
            'Извини, я не понимаю по собачьи',
            'Как же ты меня заебал!'
        ],
        'goroskop': [
            'Секундочку, сейчас гляну что у нас там в астрологи говорят',
            'Астрологи только что вышли, сейчас их договню и все тебе расскажу',
        ]
    }

    @staticmethod
    def get(key=None):
        if not key or key not in RandomFunMessages.messages:
            key = 'error'
        return random.choice(RandomFunMessages.messages[key])
