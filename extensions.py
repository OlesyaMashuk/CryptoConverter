import requests
import json
from config import *


class APIException(Exception):
    pass


class API:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты: {base}.')

        amount = float(amount)
        if amount < 0:
            raise APIException(f'Неверно указана сумма конвертируемой валюты {amount}. Необходимо указать положительное значение.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {quote}.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {base}.')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Неверно указана сумма конвертируемой валюты {amount}. Необходимо указать числовое значение.')


        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = float(json.loads(r.content)[keys[base]]*amount)

        return total_base