from django.shortcuts import render, get_object_or_404, redirect

from .models import OrderItem, Order
from cart.cart import Cart
from django.contrib.auth.models import User
from django.contrib import messages
from account.models import Profile
from product.models import StockProduct
from django.contrib.auth.decorators import login_required



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

        num_order = order.id
            
        messages.success(request, f'La commande N° {num_order} a été validé ...')
            
        return redirect("home")

    else:
        user_form = User.objects.filter(username=request.user).values()
        profile_form = Profile.objects.filter(user=me).values()

        context = {'cart': cart, 'user_form': user_form, 'profile_form': profile_form}

        return render(request, 'order/create_order.html', context)

        