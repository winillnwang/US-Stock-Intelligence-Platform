from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Stock, StockPrice


class StockAPITestCase(APITestCase):
    def setUp(self):
        self.stock = Stock.objects.create(
            symbol="SOXL",
            company_name="Direxion Daily Semiconductor Bull 3X Shares",
            exchange="NYSE Arca",
        )

        StockPrice.objects.create(
            stock=self.stock,
            date="2026-09-25",
            open="149.2400",
            high="153.9000",
            low="147.3900",
            close="151.4500",
            volume=55596775,
        )

    def test_stock_list_returns_200(self):
        response = self.client.get("/api/stocks/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_stock_detail_returns_404_for_unknown_symbol(self):
        response = self.client.get("/api/stocks/XXXX/")

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_stock_price_returns_400_for_invalid_limit(self):
        response = self.client.get(
            "/api/stocks/SOXL/prices/?limit=abc"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_stock_detail_returns_200_for_existing_symbol(self):
        response = self.client.get("/api/stocks/SOXL/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_stock_price_list_returns_price_data(self):
        response = self.client.get("/api/stocks/SOXL/prices/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        self.assertEqual(
            response.data[0]["close"],
            "151.4500",
        )
