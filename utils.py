from decimal import Decimal

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
