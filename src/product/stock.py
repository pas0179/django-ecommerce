from .models import Product, StockProduct


def calcul_stock():
    products = Product.objects.filter(available=True)

    lst_prod = []
    for val in products.values():
        prod_id = StockProduct.objects.filter(name_product_id=val["id"])
        total = 0
        for item in prod_id.values():
            total += item["quantity_in"] - item["quantity_out"]
        lst_prod.append((val["id"], total))

    for val in lst_prod:
        products.filter(id=val[0]).update(quantity=val[1])
    
    