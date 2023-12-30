from django.urls import path
from .views import add_order, admin_order_pdf, admin_order_detail



urlpatterns = [
    path("add_order/", add_order, name="add_order"),
    path('admin/order/<int:order_id>/', admin_order_detail, name='admin_order_detail'),
    path('admin/order/<int:order_id>/pdf/', admin_order_pdf,name="admin_order_pdf"),
]