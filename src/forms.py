from aiogram.dispatcher.filters.state import State, StatesGroup


# Forms
class WeatherForm(StatesGroup):
    latitude = State()
    longitude = State()


class PollForm(StatesGroup):
    question = State()
    option = State()


class CurrencyForm(StatesGroup):
    base_currency = State()
    output_currency = State()
    amount_to_convert = State()
