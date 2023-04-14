import requests
import json
from config import exchanges


class ConvertionException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(quote, base, amount):
        if quote == base:
            raise ConvertionException(f'Невозможно перевест валюты {base}')
        try:
            quote_ticker = exchanges[quote.lower()]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')
        try:
            base_ticker = exchanges[base.lower()]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')
        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}")
        price = json.loads(r.content)[exchanges[base.lower()]]
        total_base = price * amount
        total_base = round(total_base, 3)
        return total_base
