from django.urls import path
from .views import add_order


urlpatterns = [
    path("add_order/", add_order, name="add_order"),    
]