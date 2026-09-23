from django.db import models


class Stock(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    company_name = models.CharField(max_length=255)
    exchange = models.CharField(max_length=50, blank=True)
    sector = models.CharField(max_length=100, blank=True)
    industry = models.CharField(max_length=150, blank=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.symbol


class StockPrice(models.Model):
    stock = models.ForeignKey(
        Stock,
        on_delete=models.CASCADE,
        related_name="prices"
    )
    date = models.DateField()
    open = models.DecimalField(max_digits=12, decimal_places=4)
    high = models.DecimalField(max_digits=12, decimal_places=4)
    low = models.DecimalField(max_digits=12, decimal_places=4)
    close = models.DecimalField(max_digits=12, decimal_places=4)
    volume = models.BigIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["stock", "date"],
                name="unique_stock_price_date"
            )
        ]

    def __str__(self):
        return f"{self.stock.symbol} - {self.date}"