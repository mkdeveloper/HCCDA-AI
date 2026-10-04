class Shelf:
    products = []

    def add(self, product):
        return self.products.append(product)

def main():
    shelf1 = Shelf()
    shelf2 = Shelf()

    shelf1.add("Book")
    shelf2.add("Notebook")
    print(shelf2.products)
    print(shelf1.products)
    