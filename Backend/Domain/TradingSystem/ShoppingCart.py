from Backend.Domain.TradingSystem import StoresManager
from Backend.Domain.TradingSystem.Interfaces import IShoppingBag, IPurchaseDetails
from Backend.Domain.TradingSystem.Interfaces.IShoppingCart import IShoppingCart
from Backend.Domain.TradingSystem.ShoppingBag import ShoppingBag
from Backend.response import Response, PrimitiveParsable


class ShoppingCart(IShoppingCart):

    def __init__(self):
        self.stores_manager = StoresManager.get_instance()
        self.shopping_bags = dict()

    def add_product(self, store_id: str, product_id: str, quantity: int) -> Response[None]:
        if quantity <= 0:
            return Response(False, msg="Product's quantity must be positive!")

        # todo: check if store with store id exists + check if product with product id is within the store
        check_existence_response = self.stores_manager.check_existence(store_id, product_id)
        if not check_existence_response.sucess:
            return check_existence_response

        for bag in self.shopping_bags:
            if bag.get_store_ID() == store_id:
                if bag.product_in_bag(product_id):
                    return Response(False, msg="A product with id: " + str(product_id) + " already exists in the store's bag")
                bag.add_product(product_id, quantity)
                return self.success_adding_product(store_id, product_id)

        # no bag for store with store_id
        new_bag = ShoppingBag(self.stores_manager.get_store(store_id))
        self.shopping_bags.update({store_id, new_bag})
        new_bag.add_product(product_id, quantity)
        return self.success_adding_product(store_id, product_id)

    def success_adding_product(self, store_id, product_id):
        return Response(True, msg="Successfully added product with id: " + str(product_id) + "to cart")

    def remove_product(self, store_id: str, product_id: str) -> Response[None]:
        bag = self.shopping_bags.get(store_id)
        if bag is None:
            return Response(False, msg="There is no existing bag for store with store id: " + str(store_id))
        if bag.product_in_bag(product_id):
            bag.remove_product(product_id)
            return Response(True, msg="Successfully removed product with id: " + str(product_id) + " from cart")
        else:
            return Response(False, msg="There is no product with id: " + str(product_id) +
                                               "in the bag of store with id: " + str(store_id))

    def show_cart(self) -> Response:
        return Response[self](True, msg="Full shopping cart")

    def change_product_qunatity(self, store_id: str, product_id: str, new_amount: int) -> Response[None]:
        bag = self.shopping_bags.get(store_id)
        if bag is None:
            return Response(False, msg="There is no existing bag for store with store id: " + str(store_id))
        if bag.product_in_bag(product_id):
            bag.change_quantity(product_id, new_amount)
            return Response(True, msg="Successfully changed quantity of product with id: " + str(product_id))
        else:
            return Response(False, msg="There is no product with id: " + str(product_id) +
                                               "in the bag of store with id: " + str(store_id))

    # todo: ask about products_purchase_info - I think its a dict between store_id to tuple (product_id to purchase_type)
    def buy_products(self, products_purchase_info: dict, user) -> Response[PrimitiveParsable]:
        sum = 0
        for store_id in products_purchase_info.keys():
            result = self.shopping_bags[store_id].buy_products(products_purchase_info[store_id], user)
            if not result.success:
                return result
            sum += result.get_obj().get_val()
        return Response[PrimitiveParsable(sum)](True, msg="All purchase details are valid. The overall sum is: " + str(sum))

    #todo: complete this function
    def delete_products_after_purchase(self) -> Response[IPurchaseDetails]:
        for store_id in self.shopping_bags.keys():
            result = self.shopping_bags[store_id].delete_products_after_purchase()
            if not result.success:
                return result

    def show_bag(self, store_id: str) -> Response[IShoppingBag]:
        bag = self.shopping_bags.get(store_id)
        if bag is None:
            return Response(False, msg="No bag available for this store_id")
        return Response[self](True, msg="Shopping bag")