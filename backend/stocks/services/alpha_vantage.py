import os
from datetime import datetime
from decimal import Decimal

import requests

def transform_price(date_string, raw_price):
    price_date = datetime.strptime(date_string, "%Y-%m-%d").date()

    open_price = Decimal(raw_price["1. open"])
    high_price = Decimal(raw_price["2. high"])
    low_price = Decimal(raw_price["3. low"])
    close_price = Decimal(raw_price["4. close"])
    volume = int(raw_price["5. volume"])

    if volume < 0:
        raise ValueError("Volume cannot be negative")

    if low_price > high_price:
        raise ValueError("Low price cannot be greater than high price")

    if not (low_price <= open_price <= high_price):
        raise ValueError("Open price is outside the daily price range")

    if not (low_price <= close_price <= high_price):
        raise ValueError("Close price is outside the daily price range")

    return {
        "date": price_date,
        "open": open_price,
        "high": high_price,
        "low": low_price,
        "close": close_price,
        "volume": volume,
    }
def transform_time_series(time_series):
    clean_prices = []

    for date_string, raw_price in time_series.items():
        clean_price = transform_price(date_string, raw_price)
        clean_prices.append(clean_price)

    return clean_prices
      
def fetch_daily_prices(symbol):
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

    if not api_key:
        raise RuntimeError("ALPHA_VANTAGE_API_KEY is not configured")

    url = "https://www.alphavantage.co/query"

    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": api_key,
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    if "Error Message" in data:
        raise RuntimeError(f"Alpha Vantage error: {data['Error Message']}")

    if "Note" in data:
        raise RuntimeError(f"Alpha Vantage notice: {data['Note']}")

    if "Information" in data:
        raise RuntimeError(f"Alpha Vantage information: {data['Information']}")

    if "Time Series (Daily)" not in data:
        raise RuntimeError("Daily time series is missing from API response")

    return data   