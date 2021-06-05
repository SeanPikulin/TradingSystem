from sqlalchemy import Table, Column, String, Integer, ForeignKey, CheckConstraint, insert, Boolean, \
    ForeignKeyConstraint
from sqlalchemy.orm import mapper, relationship

from Backend.DataBase.IHandler import IHandler
from Backend.DataBase.database import Base, session
from Backend.Domain.TradingSystem.shopping_bag import ShoppingBag
from Backend.Domain.TradingSystem.shopping_cart import ShoppingCart
from Backend.Domain.TradingSystem.store import Store
from Backend.response import Response

from Backend.rw_lock import ReadWriteLock
from threading import Lock


class ProductInShoppingBag(Base):
    __tablename__ = "products_in_shopping_bags"
    product_id = Column(String(50), ForeignKey("products.product_id", ondelete="CASCADE"), primary_key=True)
    store_id = Column(String(50), primary_key=True)
    username = Column(String(30), primary_key=True)
    quantity = Column(Integer, CheckConstraint('quantity>0'))
    __table_args__ = (ForeignKeyConstraint(("username", "store_id"),
                                           ["shopping_bags.username", "shopping_bags.store_id"],
                                           "Double Trouble", ondelete="CASCADE", onupdate="CASCADE"),
                      {})


class ShoppingBagHandler(IHandler):
    _lock = Lock()
    _instance = None

    def __init__(self):
        super().__init__(ReadWriteLock(), ShoppingBag)

        self.__shopping_bags = Table("shopping_bags", Base.metadata,
                                     Column("store_id", String(50), primary_key=True),
                                     # add foreign key to stores when it will be created
                                     Column("username", String(50), ForeignKey("members.username"), primary_key=True))

        mapper(ShoppingBag, self.__shopping_bags, properties={
            "_ShoppingBag__store": relationship(Store, passive_deletes=True),
        })

    @staticmethod
    def get_instance():
        with ShoppingBagHandler._lock:
            if ShoppingBagHandler._instance is None:
                ShoppingBagHandler._instance = ShoppingBagHandler()
        return ShoppingBagHandler._instance

    def save(self, obj: ShoppingBag, **kwargs) -> Response[None]:
        self._rwlock.acquire_write()
        res = Response(True)
        try:
            stmt = insert(self.__shopping_bags).values(store_id=obj.get_store_ID(),
                                                       username=kwargs['username'])
            session.execute(stmt)

            for prod_id, product_to_quantity in obj.get_products_to_quantity().items():
                stmt = insert(Base.metadata.tables[ProductInShoppingBag.__tablename__]).values(
                    store_id=obj.get_store_ID(),
                    username=kwargs['username'],
                    product_id=prod_id,
                    quantity=product_to_quantity[1])
                session.execute(stmt)
            session.commit()
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            self._rwlock.release_write()
            return res

    def remove(self, obj: ShoppingBag, **kwargs) -> Response[None]:
        self._rwlock.acquire_write()
        res = Response(True)
        try:
            session.query(ProductInShoppingBag).filter_by(store_id=obj.get_store_ID(), username=kwargs['username']).delete()
            session.query(ShoppingBag).filter_by(store_id=obj.get_store_ID(), username=kwargs['username']).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            self._rwlock.release_write()
            return res

    def load_all(self):
        pass

    def update_quantity(self, username, store_id, product_id, new_quantity):
        self._rwlock.acquire_write()
        res = Response(True)
        try:
            product_in_bag = session.query(ProductInShoppingBag).filter_by(store_id=store_id, username=username, product_id=product_id).one()
            product_in_bag.quantity = new_quantity
            session.commit()
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            self._rwlock.release_write()
            return res

    def load_cart(self, username):
        self._rwlock.acquire_read()
        res = Response(True)
        try:
            bags: list[ShoppingBag] = session.query(ShoppingBag).filter_by(username=username).all()

            for bag in bags:
                products_in_bag: ProductInShoppingBag = session.query(ProductInShoppingBag).filter_by(username=username, store_id=bag.get_store_ID()).all()
                bag.add_product(products_in_bag.product_id, products_in_bag.quantity)

            cart = ShoppingCart()
            cart.add_bags({bag.get_store_ID(): bag for bag in bags})
            session.commit()
            res = Response(True, cart)
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            self._rwlock.release_read()
            return res


# if __name__ == "__main__":
#     bags_handler = ShoppingBagHandler.get_instance()
#     product_handler = ProductHandler.get_instance()
#     members = Table('members', Base.metadata,
#                     Column('username', String(50), primary_key=True),
#                     Column('password', String(50)),
#                     Column('is_admin', Boolean(20)),
#                     )
#     Base.metadata.create_all(engine)
    # bag = ShoppingBag(Store("store"))
    # object1 = Product("inoninoni", "katz", 2, ["Cat", "Dog"])
    # res = product_handler.save(object1, quantity=3, store_id="1")
    # if not res.succeeded():
    #     print(res.get_msg())
    # bag._products_to_quantity = {object1.get_id(): (object1, 3)}
    # res = bags_handler.save(bag, username="Me")
    # if not res.succeeded():
    #     print(res.get_msg())
    # res = bags_handler.remove(bag, username="Me")
    # if not res.succeeded():
    #     print(res.get_msg())

    # res = bags_handler.load_cart("Me")
    # if not res.succeeded():
    #     print(res.get_msg())
