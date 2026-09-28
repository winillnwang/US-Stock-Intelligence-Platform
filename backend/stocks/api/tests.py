from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from ..models import Stock, StockPrice


class StockAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123",
        )

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

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

    def test_stock_list_returns_401_without_authentication(self):
        response = self.client.get("/api/stocks/")

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_stock_detail_returns_404_for_unknown_symbol(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        response = self.client.get("/api/stocks/XXXX/")

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_stock_price_returns_400_for_invalid_limit(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        response = self.client.get(
            "/api/stocks/SOXL/prices/?limit=abc"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_stock_detail_returns_200_for_existing_symbol(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        response = self.client.get("/api/stocks/SOXL/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_stock_price_list_returns_price_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

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

    def test_stock_list_returns_200_with_authentication(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )

        response = self.client.get("/api/stocks/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
