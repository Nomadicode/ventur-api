import json
import requests
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from activities.models import Currency


class Command(BaseCommand):
    help = 'Fetches all currencies and adds them to the database'

    def handle(self, *args, **kwargs):
        url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/reference/v1.0/currencies"

        headers = {
            'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
            'x-rapidapi-key': "32f56c81aamshd1740bd281c1aa4p1d4792jsn49de59d2791b"
        }

        response = requests.request("GET", url, headers=headers)

        currencies = response.json()['Currencies']
        for currency in currencies:
            currency_data = {
                "code": currency['Code'],
                "name": currency['Code'],
                "symbol": currency['Symbol'],
                "decimal_digits": currency['DecimalDigits'],
                "decimal_separator": currency['DecimalSeparator'],
                "thousands_separator": currency['ThousandsSeparator'],
                "space_symbol": currency['SpaceBetweenAmountAndSymbol'],
                "symbol_left": currency['SymbolOnLeft']
            }
            currency, created = Currency.objects.get_or_create(**currency_data)