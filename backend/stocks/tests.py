from django.test import SimpleTestCase

from stocks.services.alpha_vantage import transform_price


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
