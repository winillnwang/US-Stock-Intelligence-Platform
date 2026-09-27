from rest_framework import serializers

from .models import Stock


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
