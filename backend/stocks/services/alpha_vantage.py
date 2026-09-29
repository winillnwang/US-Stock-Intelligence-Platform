import os
from datetime import datetime
from decimal import Decimal

import requests

from ..models import StockPrice


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


def save_price(stock, clean_price):
    stock_price, created = StockPrice.objects.update_or_create(
        stock=stock,
        date=clean_price["date"],
        defaults={
            "open": clean_price["open"],
            "high": clean_price["high"],
            "low": clean_price["low"],
            "close": clean_price["close"],
            "volume": clean_price["volume"],
        },
    )

    return stock_price, created


def save_prices(stock, clean_prices):
    created_count = 0
    updated_count = 0

    for clean_price in clean_prices:
        _, created = save_price(stock, clean_price)

        if created:
            created_count += 1
        else:
            updated_count += 1

    return {
        "created": created_count,
        "updated": updated_count,
    }


def update_stock_prices(stock):
    data = fetch_daily_prices(stock.symbol)

    time_series = data["Time Series (Daily)"]

    clean_prices = transform_time_series(time_series)

    result = save_prices(stock, clean_prices)

    return result


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
