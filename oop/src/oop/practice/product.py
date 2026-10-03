class Product:

    def __init__(self, name: str, stock: int, price: float) -> None:
        self.name = name
        self.stock = stock
        self.price = price

    def is_available(self) -> bool:
        return self.stock > 0

    def sell(self, quantity: int) -> bool:
        if quantity > self.stock:
            print(f"Not engough stock, only {self.stock} is available")
            return False
        self.stock -= quantity
        return True

    def restock(self, quantity: int) -> int:
        self.stock += quantity
        return self.stock

    def apply_discout(self, percentage: float) :
        discout = self.price * (1- percentage/100)
        self.price = discout
        return self.price

    def total(self):
        return self.stock * self.price

    def is_low_stock(self, limit: int = 5):
        if self.stock >= limit:
            return False
        else:
            return True

    def __str__(self) -> str:
        return f"The product is {self.name}, the price is {self.price} and available stock is {self.stock}."


def main():
    notebook = Product("notebook", 10, 4.50)
    # print("before discout and restocking")
    print(notebook)
    # notebook.restock(10)
    # notebook.apply_discout(10)
    # print(notebook.is_available())
    # print("after discount")
    


    print(notebook.sell(7))

    
    print(notebook.total())
    print(notebook)
    print(notebook.is_low_stock())
    # print(notebook.sell(15))
    # # print(notebook)
    # print(f"The product is {notebook.name}, the price is {notebook.price} and available stock is {notebook.stock}.")

    

