from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Stock, StockPrice
from .serializers import StockPriceSerializer, StockSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def stock_list_api(request):
    stocks = Stock.objects.all().order_by("symbol")

    serializer = StockSerializer(stocks, many=True)

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def stock_detail_api(request, symbol):
    stock = get_object_or_404(
        Stock,
        symbol=symbol.upper(),
    )

    serializer = StockSerializer(stock)

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def stock_price_list_api(request, symbol):
    limit = request.query_params.get("limit", 100)

    try:
        limit = int(limit)
    except ValueError:
        return Response(
            {"error": "limit must be an integer."},
            status=400,
        )

    if limit < 1 or limit > 100:
        return Response(
            {"error": "limit must be between 1 and 100."},
            status=400,
        )

    stock = get_object_or_404(
        Stock,
        symbol=symbol.upper(),
    )

    prices = StockPrice.objects.filter(stock=stock).order_by("-date")[:limit]

    serializer = StockPriceSerializer(
        prices,
        many=True,
    )

    return Response(serializer.data)
