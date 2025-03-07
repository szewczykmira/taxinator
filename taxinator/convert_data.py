import csv
import os
from decimal import Decimal
from taxinator.date_operation import get_previous_date

DATE = "Date"
DESCRIPTION = "Description"
INTEREST_EARNED = "Interest earned"
MONEY_IN = "Money in"


def process_row(row: dict) -> dict:
    operation_date = row[DATE]
    previous_day = get_previous_date(operation_date)
    earned = Decimal(row[MONEY_IN].replace("€", "").replace(",", ""))
    # TODO: add making request to the api
    return {
        DATE: operation_date,
        DESCRIPTION: row[DESCRIPTION],
        "Euro": str(earned),
        "Pln": 0,
    }


def generate_converted_values():
    dates = set()

    with (
        open(os.environ["DATA_SOURCE"]) as input_data,
        open("./output_euro.csv", "w") as output_data,
    ):
        reader = csv.DictReader(input_data)
        writer = csv.DictWriter(
            output_data, fieldnames=[DATE, DESCRIPTION, "Euro", "Pln"]
        )
        for row in reader:
            if row[DESCRIPTION] == INTEREST_EARNED:
                writer.writerow(process_row(row))
