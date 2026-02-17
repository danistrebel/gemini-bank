from decimal import Decimal
from datetime import datetime, timedelta

def get_exchange_rates():
    return {
        "EUR": Decimal("1.0"),
        "USD": Decimal("0.92"),
        "GBP": Decimal("1.17"),
        "CHF": Decimal("1.07"),
        "SEK": Decimal("0.088"),
        "NOK": Decimal("0.088"),
        "DKK": Decimal("0.134"),
        "PLN": Decimal("0.23"),
        "CZK": Decimal("0.040"),
        "HUF": Decimal("0.0025"),
        "RON": Decimal("0.20"),
        "BGN": Decimal("0.51")
    }

def convert_to_eur(amount, currency):
    rates = get_exchange_rates()
    if currency not in rates:
        raise ValueError(f"Currency {currency} not supported")
    
    rate = rates[currency]
    return Decimal(str(amount)) * rate

def get_next_date(date, frequency):
    if frequency == 'daily':
        return date + timedelta(days=1)
    elif frequency == 'weekly':
        return date + timedelta(weeks=1)
    elif frequency == 'monthly':
        month = date.month - 1 + 1
        year = date.year + month // 12
        month = month % 12 + 1
        day = min(date.day, [31,
            29 if year % 4 == 0 and not year % 100 == 0 or year % 400 == 0 else 28,
            31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
        return date.replace(year=year, month=month, day=day)
    elif frequency == 'yearly':
        try:
            return date.replace(year=date.year + 1)
        except ValueError:
            return date + (datetime(date.year + 1, 3, 1) - datetime(date.year, 3, 1))
    return date
