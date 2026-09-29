from io import StringIO
from unittest.mock import patch

from django.core.management import call_command, CommandError
from django.test import TestCase

from stocks.models import Stock


class UpdateStockPricesCommandTest(TestCase):
    def setUp(self):
        self.aapl = Stock.objects.create(
            symbol="AAPL",
            company_name="Apple Inc.",
        )

        self.soxl = Stock.objects.create(
            symbol="SOXL",
            company_name="Direxion Daily Semiconductor Bull 3X Shares",
        )

    @patch(
        "stocks.management.commands.update_stock_prices.update_stock_prices"
    )
    def test_updates_multiple_stocks(self, mock_update_stock_prices):
        mock_update_stock_prices.return_value = {
            "created": 1,
            "updated": 99,
        }

        stdout = StringIO()

        call_command(
            "update_stock_prices",
            "AAPL",
            "SOXL",
            stdout=stdout,
        )

        output = stdout.getvalue()

        self.assertIn(
            "AAPL: created=1, updated=99",
            output,
        )
        self.assertIn(
            "SOXL: created=1, updated=99",
            output,
        )

        self.assertEqual(
            mock_update_stock_prices.call_count,
            2,
        )

    @patch(
        "stocks.management.commands.update_stock_prices.update_stock_prices"
    )
    def test_continues_when_one_stock_update_fails(
        self,
        mock_update_stock_prices,
    ):
        mock_update_stock_prices.side_effect = [
            RuntimeError("API rate limit"),
            {
                "created": 1,
                "updated": 99,
            },
        ]

        stdout = StringIO()
        stderr = StringIO()

        call_command(
            "update_stock_prices",
            "AAPL",
            "SOXL",
            stdout=stdout,
            stderr=stderr,
        )

        self.assertIn(
            "AAPL: API rate limit",
            stderr.getvalue(),
        )

        self.assertIn(
            "SOXL: created=1, updated=99",
            stdout.getvalue(),
        )

        self.assertEqual(
            mock_update_stock_prices.call_count,
            2,
        )

    @patch(
        "stocks.management.commands.update_stock_prices.update_stock_prices"
    )
    def test_raises_error_before_updates_when_stock_does_not_exist(
        self,
        mock_update_stock_prices,
    ):
        with self.assertRaisesMessage(
            CommandError,
            "Stock XXXX does not exist",
        ):
            call_command(
                "update_stock_prices",
                "AAPL",
                "XXXX",
                "SOXL",
            )

        mock_update_stock_prices.assert_not_called()
