import os
import sys
from pathlib import Path

import django
from dotenv import load_dotenv
from stock_config import STOCK_CONFIG


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

def update_stock(symbol):
    print(f"\n=== Updating {symbol} ===")
    try:
        data = fetch_daily_prices(symbol)
    except Exception as e:
        print(f"Failed to fetch {symbol}: {e}")
        return False
    if "Time Series (Daily)" not in data:
      print(f"Failed to fetch daily prices for {symbol}")
      print("API response:", data)
      return False
    time_series = data["Time Series (Daily)"]
    clean_prices = transform_time_series(time_series)
    if not clean_prices:
      print(f"No price data returned for {symbol}")
      return False
    print("Total Records:", len(clean_prices))
    print("First Record:", clean_prices[0])
    print("Last Record:", clean_prices[-1])

    stock, created = Stock.objects.update_or_create(
    symbol=symbol,
    defaults={
        "company_name": STOCK_CONFIG[symbol]["company_name"],
        "exchange": STOCK_CONFIG[symbol]["exchange"],
        "sector": STOCK_CONFIG[symbol]["sector"],
        "industry": STOCK_CONFIG[symbol]["industry"],
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
    return True

def main():    
    if len(sys.argv) < 2:
        print("Usage: python scripts/fetch_stock_data.py <SYMBOL>")
        sys.exit(1)
    symbol = sys.argv[1].upper()
    supported_symbols = list(STOCK_CONFIG.keys())

    if symbol != "ALL" and symbol not in STOCK_CONFIG:
        print(f"Unsupported symbol: {symbol}")
        print("Supported symbols:", ", ".join(supported_symbols))
        sys.exit(1)
    if symbol == "ALL":
        completed_symbols = []
        failed_symbols = []

        for stock_symbol in supported_symbols:
            success = update_stock(stock_symbol)

            if success:
                completed_symbols.append(stock_symbol)
            else:
                failed_symbols.append(stock_symbol)

        print("\n=== Update Summary ===")
        print("Completed:", ", ".join(completed_symbols))
        print("Failed:", ", ".join(failed_symbols))
    else:
        update_stock(symbol) 
        
if __name__ == "__main__":
    main()         

