import os
import requests
from urllib.parse import urlencode, urljoin

CURRENCYBEACON_URL = "https://api.currencybeacon.com/v1/"

#
# {
#     "base": "EUR",
#     "date": "2024-03-08",
#     "meta": {
#         "code": 200,
#         "disclaimer": "Usage subject to terms: https://currencybeacon.com/terms"
#     },
#     "rates": {
#         "PLN": 4.29918938
#     },
#     "response": {
#         "base": "EUR",
#         "date": "2024-03-08",
#         "rates": {
#             "PLN": 4.29918938
#         }
#     }
# }
#
#
#


def fetch_historical_rate(date: str, base: str, to_currencies: list[str]):
    if os.environ.get("CURRENCY_BEACON_API_KEY") is None:
        raise ValueError("Currencybeacon is not configured.")

    params = urlencode(
        {
            "date": date,
            "base": base,
            "symbols": ",".join(to_currencies),
            "api_key": os.environ.get("CURRENCY_BEACON_API_KEY"),
        }
    )
    url = urljoin(CURRENCYBEACON_URL, "historical") + f"?{params}"
    response = requests.get(url)
    print(response.json())
