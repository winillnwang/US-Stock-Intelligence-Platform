from django.shortcuts import render
import pandas as pd

from .models import Stock, StockPrice


def stock_search(request):
    quick_symbols = list(
        Stock.objects.filter(
            is_featured=True
        ).values_list("symbol", flat=True)
    )
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
        "quick_symbols": quick_symbols,
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
    price_data = []
    distance_from_30_high_pct = None
    distance_from_30_low_pct = None  

    if stock is not None:
        latest_price = StockPrice.objects.filter(
            stock=stock
        ).order_by("-date").first()
        recent_prices = StockPrice.objects.filter(
            stock=stock
        ).order_by("-date")[:5]
        price_data = StockPrice.objects.filter(
        stock=stock
        ).order_by("date").values(
        "date",
        "open",
        "high",
        "low",
        "close",
        "volume",
        )

    df = pd.DataFrame(list(price_data))

    recent_5_avg_close = None
    recent_10_avg_close = None
    recent_20_avg_close = None
    chart_labels = []
    chart_close_values = []
    chart_ma_10_values = []
    chart_ma_20_values = []
    latest_change_pct = None
    recent_30_high = None
    recent_30_low = None
    return_5d_pct = None
    return_10d_pct = None
    return_20d_pct = None
    volatility_20d = None
    volume_change_pct = None
    chart_volume_values = []

    if not df.empty:
        df["close"] = df["close"].astype(float)
        df["volume"] = df["volume"].astype(float)
        df["change_pct"] = df["close"].pct_change() * 100
        latest_change_pct = round(df["change_pct"].iloc[-1],2)
        volume_change_pct = round(
            (df["volume"].iloc[-1] / df["volume"].iloc[-2] - 1) * 100, 2
        )
        return_5d_pct = round(
            (df["close"].iloc[-1] / df["close"].iloc[-6] - 1) * 100, 2
        )
        return_10d_pct = round(
            (df["close"].iloc[-1] / df["close"].iloc[-11] - 1) * 100, 2
        )
        return_20d_pct = round(
            (df["close"].iloc[-1] / df["close"].iloc[-21] - 1) * 100, 2
        )
        volatility_20d = round(
            df["change_pct"].tail(20).std(), 2
        )
        df["ma_10"] = df["close"].rolling(10).mean()
        df["ma_20"] = df["close"].rolling(20).mean()

        recent_5_avg_close = round(
            df["close"].tail(5).mean(),
            2
        )

        recent_10_avg_close = round(
            df["close"].tail(10).mean(),
            2
        )

        recent_20_avg_close = round(
            df["close"].tail(20).mean(),
            2
        )

        chart_data = df.tail(30)
        recent_30_high = round(chart_data["close"].max(),2)
        recent_30_low = round(chart_data["close"].min(),2)
        latest_close = chart_data["close"].iloc[-1]

        distance_from_30_high_pct = round((latest_close - recent_30_high) / recent_30_high * 100,2)

        distance_from_30_low_pct = round((latest_close - recent_30_low) / recent_30_low * 100,2)

        chart_labels = chart_data["date"].astype(str).tolist()
        chart_close_values = chart_data["close"].tolist()
        chart_ma_10_values = chart_data["ma_10"].tolist()
        chart_ma_20_values = chart_data["ma_20"].tolist()
        chart_volume_values = chart_data["volume"].tolist()

    trend_signal = None

    if (
        recent_5_avg_close is not None
        and recent_10_avg_close is not None
       ):
        if recent_5_avg_close > recent_10_avg_close:
            trend_signal = "短期股價高於 10 日平均線"
        else:
            trend_signal = "短期股價未高於 10 日平均線"

    context = {
        "symbol": symbol,
        "stock": stock,
        "latest_price": latest_price,
        "recent_prices": recent_prices,
        "recent_5_avg_close": recent_5_avg_close,
        "recent_10_avg_close": recent_10_avg_close,
        "recent_20_avg_close": recent_20_avg_close,
        "trend_signal": trend_signal,
        "chart_labels": chart_labels,
        "chart_close_values": chart_close_values,
        "chart_ma_10_values": chart_ma_10_values,
        "chart_ma_20_values": chart_ma_20_values,
        "latest_change_pct": latest_change_pct,
        "return_5d_pct": return_5d_pct,
        "return_10d_pct": return_10d_pct,
        "return_20d_pct": return_20d_pct,
        "volatility_20d": volatility_20d,
        "volume_change_pct": volume_change_pct,
        "recent_30_high": recent_30_high,
        "recent_30_low": recent_30_low,
        "distance_from_30_high_pct": distance_from_30_high_pct,
        "distance_from_30_low_pct": distance_from_30_low_pct,
        "chart_volume_values": chart_volume_values,
    }

    return render(
        request,
        "stocks/stock_detail.html",
        context,
    )
