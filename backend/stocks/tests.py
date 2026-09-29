from unittest.mock import patch

from django.test import SimpleTestCase

from stocks.services.alpha_vantage import (
    transform_price,
    transform_time_series,
    update_stock_prices,
)


class TransformPriceTest(SimpleTestCase):
    def test_raises_error_when_required_field_is_missing(self):
        raw_price = {
            "1. open": "100.00",
            "2. high": "110.00",
            "3. low": "90.00",
            "5. volume": "1000",
        }

        with self.assertRaisesMessage(
            ValueError,
            "Missing required field: 4. close",
        ):
            transform_price(
                "2026-09-29",
                raw_price,
            )

    def test_raises_error_when_price_value_is_invalid(self):
        raw_price = {
            "1. open": "invalid",
            "2. high": "110.00",
            "3. low": "90.00",
            "4. close": "105.00",
            "5. volume": "1000",
        }

        with self.assertRaises(ValueError):
            transform_price(
                "2026-09-29",
                raw_price,
            )

    def test_raises_error_when_volume_is_negative(self):
        raw_price = {
            "1. open": "100.00",
            "2. high": "110.00",
            "3. low": "90.00",
            "4. close": "105.00",
            "5. volume": "-1000",
        }

        with self.assertRaisesMessage(
            ValueError,
            "Volume cannot be negative",
        ):
            transform_price(
                "2026-09-29",
                raw_price,
            )

    def test_raises_error_when_low_is_greater_than_high(self):
        raw_price = {
            "1. open": "100.00",
            "2. high": "90.00",
            "3. low": "110.00",
            "4. close": "105.00",
            "5. volume": "1000",
        }

        with self.assertRaisesMessage(
            ValueError,
            "Low price cannot be greater than high price",
        ):
            transform_price(
                "2026-09-29",
                raw_price,
            )

    def test_raises_error_when_open_is_outside_daily_range(self):
        raw_price = {
            "1. open": "120.00",
            "2. high": "110.00",
            "3. low": "90.00",
            "4. close": "105.00",
            "5. volume": "1000",
        }

        with self.assertRaisesMessage(
            ValueError,
            "Open price is outside the daily price range",
        ):
            transform_price(
                "2026-09-29",
                raw_price,
            )

    def test_raises_error_when_close_is_outside_daily_range(self):
        raw_price = {
            "1. open": "100.00",
            "2. high": "110.00",
            "3. low": "90.00",
            "4. close": "120.00",
            "5. volume": "1000",
        }

        with self.assertRaisesMessage(
            ValueError,
            "Close price is outside the daily price range",
        ):
            transform_price(
                "2026-09-29",
                raw_price,
            )


class TransformTimeSeriesTest(SimpleTestCase):
    def test_raises_error_when_time_series_is_empty(self):
        with self.assertRaisesMessage(
            ValueError,
            "Time series cannot be empty",
        ):
            transform_time_series({})

    def test_skips_invalid_price_record(self):
        time_series = {
            "2026-09-29": {
                "1. open": "100.00",
                "2. high": "110.00",
                "3. low": "90.00",
                "4. close": "105.00",
                "5. volume": "1000",
            },
            "2026-09-28": {
                "1. open": "invalid",
                "2. high": "110.00",
                "3. low": "90.00",
                "4. close": "105.00",
                "5. volume": "1000",
            },
        }

        result = transform_time_series(time_series)

        self.assertEqual(len(result), 1)
        self.assertEqual(
            result[0]["date"].isoformat(),
            "2026-09-29",
        )

    def test_raises_error_when_all_price_records_are_invalid(self):
        time_series = {
            "2026-09-29": {
                "1. open": "invalid",
                "2. high": "110.00",
                "3. low": "90.00",
                "4. close": "105.00",
                "5. volume": "1000",
            },
            "2026-09-28": {
                "1. open": "100.00",
                "2. high": "80.00",
                "3. low": "90.00",
                "4. close": "85.00",
                "5. volume": "1000",
            },
        }

        with self.assertRaisesMessage(
            ValueError,
            "No valid price records found",
        ):
            transform_time_series(time_series)

    def test_logs_warning_when_invalid_price_record_is_skipped(self):
        time_series = {
            "2026-09-29": {
                "1. open": "100.00",
                "2. high": "110.00",
                "3. low": "90.00",
                "4. close": "105.00",
                "5. volume": "1000",
            },
            "2026-09-28": {
                "1. open": "invalid",
                "2. high": "110.00",
                "3. low": "90.00",
                "4. close": "105.00",
                "5. volume": "1000",
            },
        }

        with self.assertLogs(
            "stocks.services.alpha_vantage",
            level="WARNING",
        ) as log_context:
            transform_time_series(time_series)

        self.assertIn(
            "Skipping invalid price record for 2026-09-28",
            log_context.output[0],
        )


class UpdateStockPricesTest(SimpleTestCase):
    @patch("stocks.services.alpha_vantage.save_prices")
    @patch("stocks.services.alpha_vantage.transform_time_series")
    @patch("stocks.services.alpha_vantage.fetch_daily_prices")
    def test_logs_start_and_completion(
        self,
        mock_fetch_daily_prices,
        mock_transform_time_series,
        mock_save_prices,
    ):
        stock = type(
            "StockStub",
            (),
            {"symbol": "AAPL"},
        )()

        mock_fetch_daily_prices.return_value = {"Time Series (Daily)": {}}

        mock_transform_time_series.return_value = [{"date": "2026-09-29"}]

        mock_save_prices.return_value = {
            "created": 1,
            "updated": 99,
        }

        with self.assertLogs(
            "stocks.services.alpha_vantage",
            level="INFO",
        ) as log_context:
            update_stock_prices(stock)

        self.assertIn(
            "Starting stock price update for AAPL",
            log_context.output[0],
        )

        self.assertIn(
            "Completed stock price update for AAPL: created=1 updated=99",
            log_context.output[1],
        )

    @patch("stocks.services.alpha_vantage.fetch_daily_prices")
    def test_logs_error_when_update_fails(
        self,
        mock_fetch_daily_prices,
    ):
        stock = type(
            "StockStub",
            (),
            {"symbol": "AAPL"},
        )()

        mock_fetch_daily_prices.side_effect = RuntimeError(
            "API rate limit"
        )

        with self.assertLogs(
            "stocks.services.alpha_vantage",
            level="ERROR",
        ) as log_context:
            with self.assertRaisesMessage(
                RuntimeError,
                "API rate limit",
            ):
                update_stock_prices(stock)

        self.assertIn(
            "Stock price update failed for AAPL: API rate limit",
            log_context.output[0],
        )
