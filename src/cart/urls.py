from django.urls import path

from .views import cart_detail, cart_add, cart_update, cart_delete


urlpatterns = [
    path("details/", cart_detail, name="cart_detail"),
    path("add/", cart_add, name="cart_add"),
    path("update/", cart_update, name="cart_update"),
    path("delete/", cart_delete, name="cart_delete"),
]