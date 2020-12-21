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


""" Task 2:
Airline / Hotel Reservation System - Create a reservation system which books airline seats or hotel rooms. It charges 
various rates for particular sections of the plane or hotel. Example, first class is going to cost more than coach. 
Hotel rooms have penthouse suites which cost more. Keep track of when rooms will be available and can be scheduled.
"""
import datetime


class Item:
    u"""Represent a something that can be booked."""
    _id = 0

    def __init__(self, name: str, price=0.0):
        self.name = name
        self.price = price
        self.id = Item._id
        Item._id += 1

    def __repr__(self):
        return "BookableItem: {}, id: {}".format(self.name, self._id)


class ReservationSystem:

    def __init__(self):
        self.items = set()

    def reserve(self, item):
        u"""Book an item."""

    def available(self):
        u"""Show all available items (not booked)."""
