from django.conf import settings
from django.db import models
from django.urls import reverse
from product.models import Product


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order_user')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_order = models.DecimalField(max_digits=5, decimal_places=2)
    order_key = models.CharField(max_length=200)
    paid_status = models.BooleanField(default=False)
    # Ajout de stripe_id pour ajouter le N° de paiement retourner par stripe 
    stripe_id = models.CharField(max_length=250, blank=True)

    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return str(self.created)
    
    def get_total_cost(self):
        """Retourne le total a payer grace a la fonction get_cost dans class OrderItem"""
        return sum(item.get_cost() for item in self.items.all())
    
    def get_absolute_url(self):
        return reverse('order_list_by_order', args=[self.id])
    
    def get_stripe_url(self):
        """
        fonction pour acceder au dashboard de stripe.com avec le N° 
        créer lors d'un reglement complet accepté depuis admin
        """
        if not self.stripe_id:
            # Pas de paiement associé
            return ''
        
        if '_test_' in settings.STRIPE_SECRET_KEY:
            # path de stripe pour les tests de paiements
            path = '/test/'

        else:
            # path de stripe pour les vrais paiements
            path = '/'

        return f'https://dashboard.stripe.com{path}payments/{self.stripe_id}'
    


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                            related_name='items',
                            on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                            related_name='order_items',
                            on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        """Retourne le total d'un produit"""
        return self.price * self.quantity
    
    def get_absolute_url(self):
        return reverse('order_detail', args=[self.order_id])