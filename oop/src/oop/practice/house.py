class House:
    rooms = 4
    
    def __init__(self, owner: str, color: str):
        self.owner = owner
        self.color = color

    def __str__(self) -> str:
        return (f"The owner is {self.owner}, the house color is {self.color}. It has {self.rooms} rooms.")

def app():
    house1 = House("Yousaf", "white")
    print(house1)
    house1.rooms = 7
    House.rooms = 2
    print(house1)
    house2 = House("Ali", "Red")
    print(house2)
    house3 = House("Haseeb", "Yellow")
    print(house3)
