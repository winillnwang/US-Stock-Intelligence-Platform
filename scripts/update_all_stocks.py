import time
from fetch_stock_data import update_stock
from stock_config import STOCK_CONFIG

supported_symbols = list(STOCK_CONFIG.keys())

def main():
    completed_symbols = []
    failed_symbols = []

    for symbol in supported_symbols:
        success = update_stock(symbol)

        if success:
            completed_symbols.append(symbol)
        else:
            failed_symbols.append(symbol)

        time.sleep(2)

    print("\n=== Batch Update Summary ===")
    print("Completed:", ", ".join(completed_symbols))
    print("Failed:", ", ".join(failed_symbols))

if __name__ == "__main__":
    main()