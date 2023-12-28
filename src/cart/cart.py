from django.shortcuts import get_object_or_404
from product.models import Product
from django.conf import settings
from decimal import Decimal



class Cart():
	"""
	Object panier pour gestion sur tout le programme
	"""
	def __init__(self, request):
		self.session = request.session

		# Get the current session key if it exists
		cart = self.session.get(settings.CART_SESSION_ID)

		# If the user is new, no session key!  Create one!
		if not cart:
			cart = self.session[settings.CART_SESSION_ID] = {}

		# Make sure cart is available on all pages of site
		self.cart = cart


	def save(self):
		"""
		Sauvegarde du panier dans la session en cours
		"""
		self.session.modified = True
		

	def add(self, product, quantity):
		"""
		Ajout d'un produit dans le panier
		"""
		product_id = str(product.id)

		if product_id in self.cart:
			self.cart[product_id]['quantity'] = quantity
		else:
			self.cart[product_id] = {'price': str(product.price), 'quantity': quantity}

		self.save()


	def __iter__(self):
		"""
		Récup des produits dans la base de données suivant le panier
		et permet d'iterer sur chaque produit du panier et d'avoir toutes les
		infos les concernants  
		"""
		product_ids = self.cart.keys()
		products = Product.objects.filter(id__in=product_ids)
		cart = self.cart.copy()

		for product in products:
			cart[str(product.id)]["product"] = product

		for item in cart.values():
			item["price"] = Decimal(item["price"])
			item["total_price"] = item["price"] * item["quantity"]
			yield item

	def __len__(self):
		"""
		Retourne le nombre de produits dans le panier
		"""
		return sum(item['quantity'] for item in self.cart.values())



	def update(self, product, qty):
		"""
		Mise a jour de la quantité pour un produit
		"""
		product_id = str(product)

		if product_id in self.cart:
			self.cart[product_id]['quantity'] = qty
			
		self.save()


	def get_subtotal_price(self):
		"""
		Retourne le total avant frais de livraison 
		"""
		return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
	

	def get_total_price(self):
		"""
		Récup du total de la commande après frais de livraison
		"""
		subtotal = sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

		if subtotal == 0:
			shipping = Decimal(0.00)
		else:
			shipping = Decimal(10.50)

		total = subtotal + Decimal(shipping)

		return total
	

	def delete(self, product):
		"""
		Supprime un produit du panier
        """
		product_id = str(product)

		if product_id in self.cart:
			del self.cart[product_id]
			self.save()


	def clear(self):
		"""
		Supprime le panier de la session
		"""
		del self.session[settings.CART_SESSION_ID]
		self.save()


