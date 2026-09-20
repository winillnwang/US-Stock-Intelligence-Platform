from django.shortcuts import render

from .models import Stock, StockPrice


def stock_search(request):
    symbol = request.GET.get("symbol", "").strip().upper()

    stock = None
    latest_price = None

    if symbol:
        stock = Stock.objects.filter(
            symbol=symbol
        ).first()

    if stock is not None:
        latest_price = StockPrice.objects.filter(
            stock=stock
        ).order_by("-date").first()

    context = {
        "symbol": symbol,
        "stock": stock,
        "latest_price": latest_price,
    }

    return render(
        request,
        "stocks/stock_search.html",
        context,
    )


def stock_detail(request, symbol):
    symbol = symbol.strip().upper()

    stock = Stock.objects.filter(
        symbol=symbol
    ).first()

    latest_price = None
    recent_prices = None

    if stock is not None:
        latest_price = StockPrice.objects.filter(
            stock=stock
        ).order_by("-date").first()

        recent_prices = StockPrice.objects.filter(
            stock=stock
        ).order_by("-date")[:5]

    context = {
        "symbol": symbol,
        "stock": stock,
        "latest_price": latest_price,
        "recent_prices": recent_prices,
    }

    return render(
        request,
        "stocks/stock_detail.html",
        context,
    )
    



