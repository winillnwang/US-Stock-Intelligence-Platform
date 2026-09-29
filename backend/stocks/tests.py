from unittest.mock import patch

import requests

from django.test import SimpleTestCase

from stocks.services.alpha_vantage import (
    fetch_daily_prices,
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


class FetchDailyPricesTest(SimpleTestCase):
    @patch("stocks.services.alpha_vantage.requests.get")
    def test_raises_runtime_error_when_request_fails(
        self,
        mock_get,
    ):
        mock_get.side_effect = requests.RequestException("Network error")

        with self.assertRaisesMessage(
            RuntimeError,
            "Failed to fetch stock data for AAPL",
        ):
            fetch_daily_prices("AAPL")

    @patch("stocks.services.alpha_vantage.requests.get")
    def test_raises_runtime_error_when_api_returns_error_message(
        self,
        mock_get,
    ):
        mock_response = mock_get.return_value
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "Error Message": "Invalid API call"
        }

        with self.assertRaisesMessage(
            RuntimeError,
            "Alpha Vantage error: Invalid API call",
        ):
            fetch_daily_prices("AAPL")

    @patch("stocks.services.alpha_vantage.requests.get")
    def test_raises_runtime_error_when_api_returns_note(
        self,
        mock_get,
    ):
        mock_response = mock_get.return_value
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "Note": "API rate limit reached"
        }

        with self.assertRaisesMessage(
            RuntimeError,
            "Alpha Vantage notice: API rate limit reached",
        ):
            fetch_daily_prices("AAPL")

    @patch("stocks.services.alpha_vantage.requests.get")
    def test_raises_runtime_error_when_api_returns_information(
        self,
        mock_get,
    ):
        mock_response = mock_get.return_value
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "Information": "API request limit reached"
        }

        with self.assertRaisesMessage(
            RuntimeError,
            "Alpha Vantage information: API request limit reached",
        ):
            fetch_daily_prices("AAPL")

    @patch("stocks.services.alpha_vantage.requests.get")
    def test_raises_runtime_error_when_daily_time_series_is_missing(
        self,
        mock_get,
    ):
        mock_response = mock_get.return_value
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "Meta Data": {}
        }

        with self.assertRaisesMessage(
            RuntimeError,
            "Daily time series is missing from API response",
        ):
            fetch_daily_prices("AAPL")

    @patch("stocks.services.alpha_vantage.requests.get")
    @patch.dict(
        "stocks.services.alpha_vantage.os.environ",
        {"ALPHA_VANTAGE_API_KEY": "test-key"},
    )
    def test_returns_daily_price_data_when_request_succeeds(
        self,
        mock_get,
    ):
        mock_response = mock_get.return_value
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "Meta Data": {
                "2. Symbol": "AAPL",
            },
            "Time Series (Daily)": {
                "2026-09-29": {
                    "1. open": "100.00",
                    "2. high": "110.00",
                    "3. low": "90.00",
                    "4. close": "105.00",
                    "5. volume": "1000",
                },
            },
        }

        result = fetch_daily_prices("AAPL")

        self.assertIn(
            "Time Series (Daily)",
            result,
        )

        mock_get.assert_called_once_with(
            "https://www.alphavantage.co/query",
            params={
                "function": "TIME_SERIES_DAILY",
                "symbol": "AAPL",
                "apikey": "test-key",
            },
            timeout=10,
        )
