from Backend.Domain.TradingSystem.member import Member
from Backend.Domain.TradingSystem.trading_system_manager import TradingSystemManager


class Admin(Member):

    def __init__(self, user, username, responsibilities=None):
        super().__init__(user, username, responsibilities)
        self.trading_system_manager = TradingSystemManager.get_instance()

    def get_any_store_purchase_history(self, store_id):
        return self.trading_system_manager.get_any_store_purchase_history(store_id)

    def get_user_purchase_history(self, user_id):
        return self.trading_system_manager.get_user_purchase_history(user_id)
