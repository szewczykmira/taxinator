from peewee import Model, SqliteDatabase, CharField, DecimalField

db = SqliteDatabase("exchange_rates.db")


class ExchangeRate(Model):
    base = CharField(max_length=5)
    to_currency = CharField(max_length=5)
    rate = DecimalField()

    class Meta:
        database = db
