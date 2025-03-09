from peewee import Model, SqliteDatabase, CharField, DecimalField, DateField
from datetime import date, timedelta
import logging
from taxinator.currencybeacon import fetch_historical_rate


log = logging.getLogger(__name__)

db = SqliteDatabase("exchange_rates.db")


class ExchangeRate(Model):
    base = CharField(max_length=5)
    to_currency = CharField(max_length=5)
    rate = DecimalField()
    date = DateField()

    class Meta:
        database = db


def get_data_from_response(response: dict) -> ExchangeRate:
    base = response.get("base")
    _date = response.get("date")
    rates = response.get("rates")
    for currency, rate in rates.items():
        print("creating object", base, _date, currency, rate)

        exchange_rate = ExchangeRate.create(
            base=base, date=_date, to_currency=currency, rate=rate
        )
        return exchange_rate


def generate_rates_for_year(year: int, base: str, to_currency: str):
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)
    current_date = start_date
    db.connect()
    while current_date <= end_date:
        date_isoformat = current_date.isoformat()
        print(f"Processing date {date_isoformat}")
        response = fetch_historical_rate(date_isoformat, base, to_currency)
        print(f"Received response {response}")
        get_data_from_response(response)
        current_date += timedelta(days=1)
