import csv
import os
from decimal import Decimal
from taxinator.date_operation import get_previous_date
from taxinator.exchange_rates import get_rate
import logging

DATE = "Date"
DESCRIPTION = "Description"
INTEREST_EARNED = "Interest earned"
MONEY_IN = "Money in"

OUTPUT_FILENAME = "./output_euro.csv"


def process_row(row: dict) -> dict:
    operation_date = row[DATE]
    previous_day = get_previous_date(operation_date)
    earned = Decimal(row[MONEY_IN].replace("€", "").replace(",", ""))
    rate = get_rate(previous_day, "EUR", "PLN")
    return {
        DATE: operation_date,
        DESCRIPTION: row[DESCRIPTION],
        "Euro": str(earned),
        "Pln": Decimal(
            earned * rate,
        ).quantize(Decimal(".01")),
    }


def generate_converted_values():
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
