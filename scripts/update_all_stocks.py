import time
from fetch_stock_data import update_stock
from stock_config import STOCK_CONFIG

supported_symbols = list(STOCK_CONFIG.keys())

def main():
    for symbol in supported_symbols:
        update_stock(symbol)
        time.sleep(2)

if __name__ == "__main__":
    main()