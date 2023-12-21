from django.urls import path
from .views import add_order, paiement_completed, paiement_canceled


urlpatterns = [
    path("add_order/", add_order, name="add_order"),
    path('completed/', paiement_completed, name='completed'),
    path('canceled/', paiement_canceled, name='canceled'),  
]