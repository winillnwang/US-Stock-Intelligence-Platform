from django.urls import path

from . import views

urlpatterns = [
    path("stocks/", views.stock_list_api, name="stock_list_api"),
]
