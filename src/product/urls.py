from django.urls import path
from .views import product, category


urlpatterns = [
    path('product/<int:pk>', product, name='product'),
    path('category/<slug:slug>', category, name='category'),
]