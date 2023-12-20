from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from product.models import Product
from django.contrib import messages

from django.http import JsonResponse



def cart_detail(request):
	# Detail du panier
	cart = Cart(request)
	
	return render(request, "cart/cart_detail.html", {"cart": cart})


def cart_add(request):
	# Fonction pour ajouter un produit dans le panier
	# Recupère le panier
	cart = Cart(request)
	
	# test for POST
	if request.POST.get('action') == 'post':
		# Récup product-id et quantity
		product_id = int(request.POST.get('product_id'))

		product_qty = int(request.POST.get('product_qty'))

		# Recherche du produit dans la base de données
		product = get_object_or_404(Product, id=product_id)

		if product.available:
			if product_qty <= product.quantity:

				if product_qty > 1:

					# Sauvegarde dans la session
					cart.add(product=product, quantity=product_qty)

					# Récup de quantité d'articles dans le panier
					cart_quantity = cart.__len__()

					message = "Produits ajoutés dans votre panier"
					response = JsonResponse({'qty': cart_quantity, "message": message})
					return response
				else:
					# Sauvegarde dans la session
					cart.add(product=product, quantity=product_qty)

					# Récup de quantité d'articles dans le panier
					cart_quantity = cart.__len__()

					message = "Produit ajouté dans votre panier"
					response = JsonResponse({'qty': cart_quantity, "message": message})
					return response

			
			else:
				message = "La quantité selectionné est supérieur a la quantité disponible ..."
				response = JsonResponse({"message": message})
				return response
			
		else:
			message = "Désolé, le produit n'est plus disponible ..."
			response = JsonResponse({"message": message})
			return response
			


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        cart.delete(product=product_id)

        cart_quantity = cart.__len__()
        carttotal = cart.get_total_price()
        response = JsonResponse({'quantity': cart_quantity, 'subtotal': carttotal})
        return response


def cart_update(request):

	cart = Cart(request)
	if request.POST.get('action') == 'post':
		product_id = int(request.POST.get('productid'))
		product_qty = int(request.POST.get('productqty'))

		cart.update(product=product_id, qty=product_qty)

		cart_quantity = cart.__len__()
		cartsubtotal = cart.get_subtotal_price()
		response = JsonResponse({'quantity': cart_quantity, 'subtotal': cartsubtotal})
		return response