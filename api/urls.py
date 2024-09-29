from django.urls import path
from .views import add_order

urlpatterns = [
    path("orders/", add_order)
]