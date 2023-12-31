from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.conf import settings
from decimal import Decimal

from order.models import Order
from product.models import StockProduct, Product
from product.stock import calcul_stock_product

import stripe

# Création de l'instance stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

# Create your views here.


def payment_process(request):
    # Récup du N° de commande dans la session
    order_id = request.session.get('order_id', None)
    # Récup de l'objet order avec son id
    order = get_object_or_404(Order, id=order_id)

    # Si paiement complet alors
    success_url = request.build_absolute_uri(reverse('completed'))
    # Si paiement annnulé ou autre problème
    cancel_url = request.build_absolute_uri(reverse('canceled'))

    # Session stripe pour reglement
    session_data = {
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': [],
            'shipping_options': [],
    }

    # Ajout des produits et infos sur la session Stripe paiement
    for item in order.items.all():
        session_data['line_items'].append({
            'price_data': {
                'unit_amount': int(item.price * Decimal('100')),
                'currency': 'eur',
                'product_data': {
                    'name': item.product.name,
                },
            },
            'quantity': item.quantity,
                
        })

        session_data['shipping_options'].append({
            "shipping_rate_data": {
                    "type": "fixed_amount",
                    "fixed_amount": {"amount": 1050, "currency": "eur"},
                    "display_name": "Base1",
                    "delivery_estimate": {
                    "minimum": {"unit": "business_day", "value": 2},
                    "maximum": {"unit": "business_day", "value": 5},
                    },
            },
        })  

        # Création d'une session pour le reglement
        session = stripe.checkout.Session.create(**session_data)
        # Redirect sur formulaire stripe pour reglement
        return redirect(session.url, code=303)


def payment_completed(request):
    # Récup du N° de commande dans la session
    order_id = request.session.get('order_id', None)
    # Récup de l'objet order avec son id
    order = get_object_or_404(Order, id=order_id)

    # Une fois le reglement accepté on sort la quantité vendu pour chaque produit
    # dans stockproduct et on lance la fonction de calcul du stock pour ce(s) produit(s)
    for item in order.items.all():
        product_name = get_object_or_404(Product, name=item.product.name)
        if product_name:
            # Ajouter la quantité vendue dans la gestion du stock
            StockProduct.objects.create(name_product=product_name,
                                        # Sortie de stock du produit
                                        quantity_out=item.quantity,
                                        )
        
            # Envoi le N° du produit pour recalculé son stock
            calcul_stock_product(product_name.id)

    return render(request, 'payment/completed.html')


def payment_canceled(request):     
    return render(request, 'payment/canceled.html')
