Convert currencies from financial statement using historical data.

It consists of two parts:
1. Fetching historical exchange rates from the previous year and stores them in a db.
2. Process financial statement and saves the output.

## Installation

1. `uv install`
2. Set env variables:
```shell
export DATA_SOURCE=...
export CURRENCY_BEACON_API_KEY=...
```

## Fetching historical exchange rates:
1. Make sure you have installed packages and env variables are set
2. Update script `generate_rates` with correct values -> year / base currency / output currency
3. Run `python3 generate_rates.py`


## Processing financial statements
1. Make sure you have installed packages and env variables are set
2. Make sure `DATA_SOURCE` points to a correct input file
3. The input file should have these columns: 
   1. Date
   2. Description
   3. Money in
4. Run `python3 generate_rates.py`




## Further plans for development
There is no plans for the future. Hopefully I won't have to run it more than once a year, so I don't see a need to update it any furhter, but if I did I would:
1. Add parameters to `generate_rates` script. They should be taken from the command line.
2. Pass input file as a parameter for `convert` script.
3. Add more tests
