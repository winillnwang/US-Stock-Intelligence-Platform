import time
from fetch_stock_data import update_stock
from stock_config import STOCK_CONFIG
from datetime import datetime
from pathlib import Path

supported_symbols = list(STOCK_CONFIG.keys())

def main():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / f"stock_update_{datetime.now():%Y%m%d}.log"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"\n=== Batch Update Started: {datetime.now()} ===\n")
        
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
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write("=== Batch Update Summary ===\n")
        f.write(f"Completed: {', '.join(completed_symbols)}\n")
        f.write(f"Failed: {', '.join(failed_symbols)}\n")

if __name__ == "__main__":
    main()