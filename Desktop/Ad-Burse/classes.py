from aiogram.dispatcher.filters.state import StatesGroup, State


class Answer(StatesGroup):
    message_age_interval = State()
    message_country = State()
    message_stats = State()
    message_network = State()
    message_link = State()
    message_subscribers = State()

'''class USER(object):
    def __init__(self, user_id, signal, favourite):
        self.user_id = user_id
        self.signal = signal        # dict key: product value: [min, max]
        self.favourite = favourite  # list

    def add_signal(self, product, min_price, max_price):
        self.signal = {product: [min_price, max_price]}

    def add_favourite(self, favourite):
        self.favourite = self.favourite.append(favourite)
'''