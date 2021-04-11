from abc import ABC, abstractmethod
from Backend.Domain.TradingSystem.shopping_cart import ShoppingCart
from Backend.response import Response


class UserState(ABC):
    def __init__(self, user, cart=None):
        if cart is None:
            cart = ShoppingCart()
        self.cart = cart
        self.user = user

    def set_user(self, user):
        self.user = user

    @abstractmethod
    def get_username(self):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def login(self, username, password):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def register(self, username, password):
        return Response(False, msg="Abstract Method")

    def save_product_in_cart(self, store_id, product_id, quantity):
        return self.cart.add_product(store_id, product_id, quantity)

    def show_cart(self):
        return Response[ShoppingCart](True, obj=self.cart, msg="got cart successfully")

    def delete_from_cart(self, store_id, product_id):
        return self.cart.remove_product(store_id, product_id)

    def change_product_quantity_in_cart(self, store_id, product_id, new_amount):
        return self.cart.change_product_quantity(store_id, product_id, new_amount)

    def buy_cart(self, current_user):
        return self.cart.buy_products(current_user)

    def get_cart_price(self):
        return self.cart.get_price()

    @abstractmethod
    def delete_products_after_purchase(self):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def open_store(self, store_name):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def get_purchase_history(self):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def add_new_product(self, store_id, product_name, product_price, quantity):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def remove_product(self, store_id, product_id):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def change_product_quantity_in_store(self, store_id, product_id, new_quantity):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def edit_product_details(self, store_id, product_id, new_name, new_price):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def appoint_new_store_owner(self, store_id, new_owner):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def appoint_new_store_manager(self, store_id, new_manager):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def add_manager_permission(self, store_id, username, permission):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def remove_manager_permission(self, store_id, username, permission):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def remove_appointment(self, store_id, username):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def get_store_personnel_info(self, store_id):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def get_store_purchase_history(self, store_id):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def get_any_store_purchase_history_admin(self, store_id):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def get_user_purchase_history_admin(self, username):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def is_appointed(self, store_id):
        return Response(False, msg="Abstract Method")
