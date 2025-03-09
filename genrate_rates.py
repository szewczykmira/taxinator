import logging
from datetime import date, timedelta

from taxinator.currencybeacon import fetch_historical_rate
from taxinator.exchange_rates import ExchangeRate, db

logging.basicConfig(level=logging.INFO)


def get_data_from_response(response: dict) -> ExchangeRate:
    base = response.get("base")
    _date = response.get("date")
    rates = response.get("rates")
    for currency, rate in rates.items():
        logging.info("creating object", base, _date, currency, rate)

        exchange_rate = ExchangeRate(
            base=base, date=_date, to_currency=currency, rate=rate
        )
        logging.info(f"Processing data: {_date} {base} -> {currency}: rate {rate}")
        return exchange_rate


def generate_rates_for_year(year: int, base: str, to_currency: str):
    """Generating historical exchange rate for a whole year at once. It saves it in the db."""
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)
    current_date = start_date
    db.connect()
    rates = []
    logging.info("Start generating rates")
    while current_date <= end_date:
        date_isoformat = current_date.isoformat()
        logging.info(f"Processing date {date_isoformat}")
        response = fetch_historical_rate(date_isoformat, base, to_currency)
        logging.info(f"Received response {response}")
        rates.append(get_data_from_response(response))
        current_date += timedelta(days=1)
    ExchangeRate.bulk_create(rates)
    logging.info("Finished. All rates are saved in the db.")


if __name__ == "__main__":
    generate_rates_for_year(2024, "eur", "pln")
