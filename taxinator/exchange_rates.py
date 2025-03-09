from datetime import date
from decimal import Decimal

from peewee import CharField, DateField, DecimalField, Model, SqliteDatabase

db = SqliteDatabase("exchange_rates.db")


class ExchangeRate(Model):
    base = CharField(max_length=5)
    to_currency = CharField(max_length=5)
    rate = DecimalField()
    date = DateField()

    class Meta:
        database = db


def get_rate(_date: date, base_currency: str, to_currency: str) -> Decimal:
    return ExchangeRate.get(
        ExchangeRate.date == _date,
        ExchangeRate.base == base_currency,
        ExchangeRate.to_currency == to_currency,
    ).rate
