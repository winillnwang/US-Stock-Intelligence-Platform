import os
import sys
from pathlib import Path

import django
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = BASE_DIR / "backend"

sys.path.append(str(BACKEND_DIR))

load_dotenv(BASE_DIR / ".env")

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django.setup()

from stocks.models import Stock, StockPrice
from stocks.services.alpha_vantage import (
    fetch_daily_prices,
    transform_time_series,
)
if len(sys.argv) < 2:
    print("Usage: python scripts/fetch_stock_data.py <SYMBOL>")
    sys.exit(1)

symbol = sys.argv[1].upper()
company_names = {
    "AAPL": "Apple Inc.",
    "SOXL": "Direxion Daily Semiconductor Bull 3X Shares",
}
supported_symbols = list(company_names.keys())
if symbol != "ALL" and symbol not in company_names:
    print(f"Unsupported symbol: {symbol}")
    print("Supported symbols:", ", ".join(supported_symbols))
    sys.exit(1)
def update_stock(symbol):
    print(f"\n=== Updating {symbol} ===")
    try:
        data = fetch_daily_prices(symbol)
    except Exception as e:
        print(f"Failed to fetch {symbol}: {e}")
        return
    if "Time Series (Daily)" not in data:
      print(f"Failed to fetch daily prices for {symbol}")
      print("API response:", data)
      return
    time_series = data["Time Series (Daily)"]
    clean_prices = transform_time_series(time_series)
    if not clean_prices:
      print(f"No price data returned for {symbol}")
      return
    print("Total Records:", len(clean_prices))
    print("First Record:", clean_prices[0])
    print("Last Record:", clean_prices[-1])

    stock, created = Stock.objects.get_or_create(
        symbol=symbol,
        defaults={
            "company_name": company_names[symbol],
        },
    )

    print("Stock:", stock)
    print("Created:", created)

    created_count = 0
    updated_count = 0

    for clean_price in clean_prices:
        stock_price, price_created = StockPrice.objects.update_or_create(
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

        if price_created:
            created_count += 1
        else:
            updated_count += 1
    print("Latest Date:", clean_prices[0]["date"])
    print("Created Prices:", created_count)
    print("Updated Prices:", updated_count)
    print(f"Completed: {symbol}")
    
if symbol == "ALL":
    for stock_symbol in supported_symbols:
        update_stock(stock_symbol)
else:
    update_stock(symbol)    

