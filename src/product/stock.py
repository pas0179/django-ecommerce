from .models import Product, StockProduct


def calcul_stock_product(product_id):

    prod = Product.objects.filter(id=product_id)

    lst_prod = []
    # Récup des données dans base stockproduct
    for val in prod.values():
        prod_id = StockProduct.objects.filter(name_product_id=val["id"])
        total = 0
        for item in prod_id.values():
            total += item["quantity_in"] - item["quantity_out"]
        lst_prod.append((val["id"], total))

    for val in lst_prod:
        prod.filter(id=val[0]).update(quantity=val[1])



    for val in prod.values():
        """
        Si la quantité est a 0 alors le produit n'est plus disponible
        """

        if val["quantity"] == 0:           
            prod.filter(id=val["id"]).update(available=False)
        else:
            prod.filter(id=val["id"]).update(available=True)




