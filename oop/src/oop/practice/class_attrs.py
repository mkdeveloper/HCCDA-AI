class Product:
    currency: str = "USD"
    product_counter: int = 0

    def __init__(self, name: str, price: float, stock: int) -> None:
        self.name = name
        self.price = price
        self.stock = stock
        Product.product_counter = Product.product_counter + 1

    def __str__(self) -> str:
        return f"{self.name}, the price is {self.price} {self.currency} and the available stock is {self.stock}."


def myproduct():
    notebook = Product("Notebook", 30.5, 50)
    backpack = Product("Backpack", 300.50, 60)
    pen = Product("Pen", 10, 100)

    print(notebook)
    print(backpack)
    print(pen)
    print(f"The total number of products are {Product.product_counter}")

    notebook.currency = "EUR"
    Product.currency = "PKR"
    print(notebook)
    print(backpack)
    print(pen)