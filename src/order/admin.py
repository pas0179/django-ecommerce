from django.contrib import admin

from .models import Order, OrderItem

# Register your models here.

class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["product"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'paid_status', 'total_order', 'order_key',
        'created', 'updated']
    list_filter = ['paid_status', 'created', 'updated']
    inlines = [OrderItemInLine]
