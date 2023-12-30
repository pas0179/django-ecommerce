from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse

from .models import Order, OrderItem
import csv
import datetime
from django.http import HttpResponse

# Register your models here.


def export_to_csv(modeladmin, request, queryset):

    opts = modeladmin.model._meta
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
                
            data_row.append(value)
        writer.writerow(data_row)
    return response
            
export_to_csv.short_description = 'Export to CSV'


def order_detail(obj):
    """
    Ajoute un bouton detail pour chaque commande
    Affiche: nom, prénom, adresse, mail, produits et total
    """
    url = reverse('admin_order_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">Voir</a>')


def order_payment(obj):
    """
    Ajout depuis mise en place stripe pour depuis le N° de reglement de stripe
    retourné sur le dashboard stripe.com
    """
    url = obj.get_stripe_url()
    if obj.stripe_id:
        html = f'<a href="{url}" target="_blank">{obj.stripe_id}</a>'
        return mark_safe(html)
    return ''

order_payment.short_description = 'Reglement Stripe'


def order_pdf(obj):
    """
    Génération d'un pdf pour chaque commande réglé
    """
    url = reverse('admin_order_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')

order_pdf.short_description = 'Facture'


class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["product"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', order_detail, order_pdf, 'paid_status', 'total_order']
    list_filter = ['paid_status', 'created', 'updated']
    inlines = [OrderItemInLine]
    actions = [export_to_csv]
