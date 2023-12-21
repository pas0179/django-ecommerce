from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.conf import settings
from decimal import Decimal

from .models import OrderItem, Order
from cart.cart import Cart
from django.contrib.auth.models import User
from django.contrib import messages
from account.models import Profile
from product.models import StockProduct
from django.contrib.auth.decorators import login_required

from .task import order_created

import stripe

# Création de l'instance stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION



@login_required
def add_order(request):
    """Vue pour la commande des produits"""
    # On apppelle le contenu du panier dans une variable
    cart = Cart(request)
    user = request.user

    me = User.objects.get(username=user)

    if request.method == 'POST':
        # Création du formulaire
        total = cart.get_total_price()

        order = Order.objects.create(user=me, 
                                    total_order=total)
        for item in cart:
            OrderItem.objects.create(order=order,
                                    product=item['product'],
                                    price=item['price'],
                                    quantity=item['quantity'],
                                    )
                
            # Ajouter la quantité vendue dans la gestion du stock
            StockProduct.objects.create(name_product=item['product'],
                                        # Sortie de stock du produit
                                        quantity_out=item['quantity'],
                                        )
        # Vide le panier
        cart.clear()

        # Lancement d'une tache insynchrone pour l'envoi d'un mail
        # au client pour la commande
        order_created.delay(order.id, user.first_name, user.username)

        # Ajoute le N° de commande dans la session
        # request.session['order_id'] = order.id

        # redirect sur reglement
        # return redirect(reverse('process'))

        # Création de la session pour reglement
        num_order = order.id
        order = get_object_or_404(Order, id=num_order)

        success_url = request.build_absolute_uri(reverse('completed'))
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

        # add order items to the Stripe checkout session
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
            
        # messages.success(request, f'La commande N° {num_order} a été validé ...')
            
        # return redirect("home")

    else:
        user_form = User.objects.filter(username=request.user).values()
        profile_form = Profile.objects.filter(user=me).values()

        context = {'cart': cart, 'user_form': user_form, 'profile_form': profile_form}

        return render(request, 'order/create_order.html', context)
    

def paiement_completed(request):
    return render(request, 'order/completed.html')


def paiement_canceled(request):
    return render(request, 'order/canceled.html')

        