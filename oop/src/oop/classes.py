class Car:
    def __init__( self, brand: str, model:str, color: str) -> None:
        self.brand = brand
        self.model = model
        self.color = color


    def new_color(self, color: str) -> str:
        self.color = color
        return self.color

def main():
    car_1 = Car("Toyata", "City", "red")    
    car_2 = Car("Honda", "Civic", "red")

    car_1.model = "bmw"
    # print(car_1.color)
    # print(car_1)
    print(f"Car 1 Brand: {car_1.brand} color: {car_1.color} model: {car_1.model}")
    print(f"Car 2 Model: {car_2.model}")
    