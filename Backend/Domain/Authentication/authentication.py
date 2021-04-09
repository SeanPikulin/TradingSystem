from Backend.Domain.DBHandler import DBHandler
from abc import ABC, abstractmethod
from Backend import response
from Backend.UnitTests.authentication.DBHandlerMock import DBHandlerMock

class IAuthentication():

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'register') and
                callable(subclass.register) and
                hasattr(subclass, 'login') and
                callable(subclass.login)and
                hasattr(subclass, 'create_DBHandler') and
                callable(subclass.create_DBHandler) and
                hasattr(subclass, 'set_mock') and
                callable(subclass.set_mock))

    def create_DBHandler(self,is_mock):
        return DBHandlerMock() if is_mock else DBHandler()

    def set_mock(self):
        self.use_mock = True

class Authentication(IAuthentication):
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if Authentication.__instance is None:
            Authentication()
        return Authentication.__instance

    def __init__(self,is_mock):
        """ Virtually private constructor. """
        if Authentication.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Authentication.__instance = self
            self.db_handler = IAuthentication.create_DBHandler(self,is_mock)

    def register(self, username, password):
        if self.db_handler.is_username_exists(username=username):
            return response.Response[None](success=False, msg="username already exists")

        else:
            self.db_handler.add_user_to_db(username=username, password=password)
            return response.Response[None](success=True, msg="registration succeeded")

    def login(self, username, password):
        if not self.db_handler.is_username_exists(username=username):
            return response.Response[None](success=False, msg="username doesn't exist in the system")

        else:
            if not self.db_handler.is_password_match(given_password=password, username=username):
                return response.Response[None](success=False, msg="password incorrect")

            else:
                is_admin = self.db_handler.is_username_admin(username=username)
                return response.Response[None](success=True,obj=response.PrimitiveParsable(is_admin),msg="login succeeded")


