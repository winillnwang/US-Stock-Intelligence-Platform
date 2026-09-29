import time

from django.core.management.base import BaseCommand, CommandError

from stocks.models import Stock
from stocks.services.alpha_vantage import update_stock_prices


class Command(BaseCommand):
    help = "Update stock prices from Alpha Vantage"

    def add_arguments(self, parser):
        parser.add_argument("symbols", nargs="+", type=str)

    def handle(self, *args, **options):
        symbols = [symbol.upper() for symbol in options["symbols"]]

        stocks = []

        for symbol in symbols:
            try:
                stock = Stock.objects.get(symbol=symbol)
            except Stock.DoesNotExist:
                raise CommandError(f"Stock {symbol} does not exist")

            stocks.append(stock)

        for index, stock in enumerate(stocks):
            result = update_stock_prices(stock)

            self.stdout.write(
                self.style.SUCCESS(
                    f"{stock.symbol}: "
                    f"created={result['created']}, "
                    f"updated={result['updated']}"
                )
            )

            if index < len(stocks) - 1:
                time.sleep(1)
