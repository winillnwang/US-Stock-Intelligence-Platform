from django.core.management.base import BaseCommand, CommandError

from stocks.models import Stock
from stocks.services.alpha_vantage import update_stock_prices


class Command(BaseCommand):
    help = "Update stock prices from Alpha Vantage"

    def add_arguments(self, parser):
        parser.add_argument("symbol", type=str)

    def handle(self, *args, **options):
        symbol = options["symbol"].upper()

        try:
            stock = Stock.objects.get(symbol=symbol)
        except Stock.DoesNotExist:
            raise CommandError(f"Stock {symbol} does not exist")

        result = update_stock_prices(stock)

        self.stdout.write(
            self.style.SUCCESS(
                f"{stock.symbol}: "
                f"created={result['created']}, "
                f"updated={result['updated']}"
            )
        )
