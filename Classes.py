"""Task: Product Inventory Project - Create an application which manages an inventory of _products.
Create a product class which has a price, id, and quantity on hand. Then create an inventory class which keeps track of
various _products and can sum up the inventory value."""
from dataclasses import dataclass


@dataclass
class Product:
    price: float
    id: int
    quantity: int


class Inventory:

    def __init__(self):
        self._products = []
        self.total_value = 0

    def __repr__(self):
        return "Inventory(products: {}, total value: {}.".format(len(self._products), self.total_value)

    def add(self, product: Product):
        self._products.append(product)
        self.total_value += product.price * product.quantity

    def remove(self, product: Product):
        try:
            self._products.remove(product)
            self.total_value -= product.price * product.quantity
        except ValueError:
            print("There is no such a product in the inventory!")
