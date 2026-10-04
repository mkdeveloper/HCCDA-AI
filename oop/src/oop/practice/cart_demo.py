class Product:
    def __init__(self, name: str, price: float, stock: int) -> None:
        self.name = name
        self.price = price
        self.stock  = stock


class CartItem:
    def __init__(self, product: Product, quantity: int) -> None:
       self.product = product
       self.quantity = quantity  

    def sub_total(self):
        return self.product.price * self.quantity

class Cart:
    def __init__(self) -> None:
        self.items = []

    def add(self, product: Product, quantity: int = 1):
        if  quantity > product.stock:
            print(f"The stock is low, available stock {product.stock}")
            return
        self.items.append(CartItem(product, quantity))

    def total(self):
        total = 0
        for item in self.items:
            total += item.sub_total()
        return total



def main():
    notebook = Product("Notebook", 4.50, 45)
    backpack = Product("Backpack", 35.00, 12)

    print(notebook.name)
    print(backpack.name)

    cart = Cart()
    cart.add(notebook, 2)
    cart.add(backpack,1)
    cart.add(notebook, 100)
    print(len(cart.items))
    print(cart.total())
    