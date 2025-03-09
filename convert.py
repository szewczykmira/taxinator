import csv
import logging
import os
from datetime import date, datetime, timedelta
from decimal import Decimal

from taxinator.exchange_rates import get_rate

# input data definition
DATE = "Date"
DESCRIPTION = "Description"
INTEREST_EARNED = "Interest earned"
MONEY_IN = "Money in"

OUTPUT_FILENAME = "./output_euro.csv"


def get_date(_date: str) -> date:
    return datetime.strptime(_date, "%b %d, %Y").date()


def get_previous_date(_date: str) -> date:
    return get_date(_date) - timedelta(days=1)


def process_row(row: dict) -> dict:
    """
    1. Retrieve important data from the csv row - operation date; earned;
    2. Use them to fetch exchange rate from the previous date;
    3. Calculate how much is that in different currency;
    4. Return formatted result
    """
    operation_date = row[DATE]
    previous_day = get_previous_date(operation_date)
    earned = Decimal(row[MONEY_IN].replace("€", "").replace(",", ""))
    rate = get_rate(previous_day, "EUR", "PLN")
    logging.info(f"Returning data for {operation_date}")
    return {
        DATE: operation_date,
        DESCRIPTION: row[DESCRIPTION],
        "Euro": str(earned),
        "Pln": Decimal(
            earned * rate,
        ).quantize(Decimal(".01")),
    }


def generate_converted_values():
    """Process data from the received file, process them and save in the output file."""
    logging.info("Start converting currencies")

    with (
        open(os.environ["DATA_SOURCE"]) as input_data,
        open(OUTPUT_FILENAME, "w") as output_data,
    ):
        reader = csv.DictReader(input_data)
        writer = csv.DictWriter(
            output_data, fieldnames=[DATE, DESCRIPTION, "Euro", "Pln"]
        )
        writer.writeheader()
        for row in reader:
            logging.debug(f"Processing row {row}")
            if row[DESCRIPTION] == INTEREST_EARNED:
                logging.debug(f"Row is not about interest earned - skipping.")
                writer.writerow(process_row(row))

        logging.info(f"Done. You can find results in {OUTPUT_FILENAME}")


logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    generate_converted_values()
