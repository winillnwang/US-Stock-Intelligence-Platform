import sys
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = BASE_DIR / "backend"

sys.path.append(str(BACKEND_DIR))

from stocks.services.alpha_vantage import (
    fetch_daily_prices,
    transform_time_series,
)


load_dotenv(BASE_DIR / ".env")

data = fetch_daily_prices("AAPL")

time_series = data["Time Series (Daily)"]
clean_prices = transform_time_series(time_series)

print("Total Records:", len(clean_prices))
print("First Record:", clean_prices[0])
print("Last Record:", clean_prices[-1])