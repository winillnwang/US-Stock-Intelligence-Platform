from django.contrib import admin

from .models import Stock, StockPrice


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("symbol", "company_name", "is_featured")
    list_editable = ("is_featured",)


@admin.register(StockPrice)
class StockPriceAdmin(admin.ModelAdmin):
    list_display = ("stock", "date", "open", "high", "low", "close", "volume")
    list_filter = ("stock", "date")
    search_fields = ("stock__symbol",)
