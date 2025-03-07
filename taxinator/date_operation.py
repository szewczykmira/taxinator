from datetime import datetime, date, timedelta


def get_date(_date: str) -> date:
    return datetime.strptime(_date, "%b %d, %Y").date()


def get_previous_date(_date: str) -> date:
    return get_date(_date) - timedelta(days=1)
