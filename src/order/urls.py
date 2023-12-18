from django.urls import path
from .views import add_order, order_list


urlpatterns = [
    path("add_order/", add_order, name="add_order"),
    path("order_list/", order_list, name="order_list"),
]