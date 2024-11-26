class Laden:
    def __init__(shop, name: any):
        shop.name = name  
        shop.products = {} 

    def addproduct(shop, product_name: any, price):
        """Adds a product to the shop"""
        if product_name in shop.products:
            print(f"Das Produkt {product_name} ist bereits im Laden.")
        else:
            shop.products[product_name] = price
            print(f"Produkt {product_name} mit dem Preis {price} wurde hinzugefügt.")

    def remove_Products(shop, product_name: any):
        """Removes a Prduct from the shop"""
        if product_name in shop.products:
            del shop.products[product_name]
            print(f"Produkt {product_name} wurde entfernt.")
        else:
            print(f"Das Produkt {product_name} ist nicht im Laden.")

    def totalValue(shop):
        """Calculates the total shop value"""
        total = sum(shop.products.values())
        print(f"Der Gesamtwert der Produkte im Laden beträgt: {total} €.")
        return total

    def showProducts(shop):
        """Shows all products"""
        if not shop.products:
            raise BaseException("Der Laden ist leer...")
        else:
            print(f"Produkte im Laden {shop.name}:")
            for product, price in shop.products.items():
                print(f"{product}: {price} €")


# ----- Beispiel Nutzung -------
shop = Laden("SuperShop")

shop.addproduct("Apfel", 1.2)
shop.addproduct("Brot", 2.5)
shop.addproduct("Milch", 1.0)

shop.showProducts()

shop.totalValue()

shop.remove_Products("Brot")

shop.showProducts()

emptyShop = Laden("BoringShop")

emptyShop.showProducts()
