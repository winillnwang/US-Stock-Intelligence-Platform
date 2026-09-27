from django.urls import path

from . import views

urlpatterns = [
    path("stocks/", views.stock_list_api, name="stock_list_api"),
    path(
        "stocks/<str:symbol>/",
        views.stock_detail_api,
        name="stock_detail_api",
    ),
    path(
        "stocks/<str:symbol>/prices/",
        views.stock_price_list_api,
        name="stock_price_list_api",
    ),
]
