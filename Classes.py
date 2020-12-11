"""Task: Product Inventory Project - Create an application which manages an inventory of _products.
Create a product class which has a price, id, and quantity on hand. Then create an inventory class which keeps track of
various _products and can sum up the inventory value."""
from dataclasses import dataclass
from typing import Union


@dataclass
class Product:
    name: str = ""
    price: float = 0.0
    id: int = -1
    quantity: int = 0


class Inventory:

    def __init__(self):
        self._products = []
        self.total_value = 0

    def __repr__(self):
        return "Inventory(products: {}, total value: {:.2f}.".format(len(self._products), self.total_value)

    def add(self, product: Union[Product, list[Product]]):
        if product is Product:
            product = list(product)
        for item in product:
            self._products.append(item)
            self.total_value += item.price * item.quantity

    def remove(self, product: Union[Product, list[Product]]):
        try:
            if product is Product:
                product = list(product)
            for item in product:
                self._products.remove(item)
                self.total_value -= item.price * item.quantity
        except ValueError:
            print("There is no such a product in the inventory!")

    def update(self):
        self.total_value = sum([x.price * x.quantity for x in self._products])

    def list_all(self):
        return ((x.name, x.id, x.price, x.quantity, round(x.price * x.quantity, 2)) for x in self._products)
