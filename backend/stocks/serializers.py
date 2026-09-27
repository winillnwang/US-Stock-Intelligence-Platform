from rest_framework import serializers

from .models import Stock, StockPrice


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = [
            "id",
            "symbol",
            "company_name",
            "exchange",
            "sector",
            "industry",
            "is_featured",
        ]


class StockPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockPrice
        fields = [
            "date",
            "open",
            "high",
            "low",
            "close",
            "volume",
        ]
