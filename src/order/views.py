from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.conf import settings

from django.contrib.auth.models import User
from account.models import Profile

from .models import OrderItem, Order
from cart.cart import Cart
from django.contrib.auth.models import User
from account.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# paquets nécessaire pour le pdf envoyer après le reglement
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint


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
                
        # Vide le panier
        cart.clear()

        # Ajoute le N° de commande dans la session
        request.session['order_id'] = order.id

        # redirect sur reglement
        return redirect(reverse('process'))

    else:
        user_form = User.objects.filter(username=request.user).values()
        profile_form = Profile.objects.filter(user=me).values()

        context = {'cart': cart, 'user_form': user_form, 'profile_form': profile_form}

        return render(request, 'order/create_order.html', context)
    

    

@staff_member_required
def admin_order_detail(request, order_id):
    """
    Change ADMIN ORDER, ajoute une vue pour avoir le détail d'une commande
    """
    order = get_object_or_404(Order, id=order_id)
    user = User.objects.filter(username=order.user).values()
    user_id = user[0]["id"]
    
    profile = Profile.objects.filter(user=user_id)

    context = {
        "order": order,
        "user": user,
        "profile": profile,
    }
    return render(request, 'admin/order/order/detail.html',context)

    

@staff_member_required
def admin_order_pdf(request, order_id):
    """
    Modifie la vue Admin pour order afin de créer les pdfs des commandes réglés
    """
    # Récup de l'objet order
    order = get_object_or_404(Order, id=order_id)

    # Récup de l'objet User
    user = User.objects.filter(username=order.user).values()
    user_id = user[0]["id"]
    
    # Récup de l'objet profile
    profile = Profile.objects.filter(user=user_id)
    
    html = render_to_string('order/pdf.html', {"order": order, "user": user, "profile": profile})

    response = HttpResponse(content_type='application/pdf')
    # Génération d'un nouveau pdf pour chaque reglement accepté
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'

    weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response,
                    stylesheets=[weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')],
                    presentational_hints=True)
    
    return response


        