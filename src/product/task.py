from celery import shared_task
from .models import Product, StockProduct


@shared_task
def calcul_stock_all_products():
    products = Product.objects.all()

    lst_prod = []
    for val in products.values():
        prod_id = StockProduct.objects.filter(name_product_id=val["id"])
        total = 0
        for item in prod_id.values():
            total += item["quantity_in"] - item["quantity_out"]
        lst_prod.append((val["id"], total))

    for val in lst_prod:
        products.filter(id=val[0]).update(quantity=val[1])
    
    
    for val in products.values():
        """
        Si la quantité est a 0 alors le produit n'est plus disponible
        """

        if val["quantity"] == 0:           
            products.filter(id=val["id"]).update(available=False)
        else:
            products.filter(id=val["id"]).update(available=True)