from abc import ABC, abstractmethod

from sqlalchemy.exc import DisconnectionError

from Backend.DataBase.database import session
from Backend.response import Response, PrimitiveParsable
from Backend.rw_lock import ReadWriteLock


class IHandler(ABC):

    def __init__(self, rwlock: ReadWriteLock, class_type):
        self._rwlock = rwlock
        self._class_type = class_type

    def save(self, obj, **kwargs) -> Response[None]:
        self._rwlock.acquire_write()
        res = Response(True)
        try:
            session.add(obj)
            session.commit()
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            self._rwlock.release_write()
            return res

    def remove(self, obj, **kwargs) -> Response[None]:
        self._rwlock.acquire_write()
        res = Response(True)
        try:
            session.delete(obj)
            session.commit()
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            self._rwlock.release_write()
            return res

    @abstractmethod
    def update(self):
        self._rwlock.acquire_write()
        res = Response(True)
        try:
            session.commit()
            res = Response(True)
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            self._rwlock.release_write()
            return res

    @abstractmethod
    def load(self, id):
        self._rwlock.acquire_read()
        res = Response(True)
        try:
            res_query = session.query(self._class_type).get(id)
            session.commit()
            res = Response(True, res_query)

        except DisconnectionError as err:
            session.rollback()
            res = Response(False, obj=PrimitiveParsable(0), msg=str(err))

        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))

        finally:
            self._rwlock.release_read()
            return res

    @abstractmethod
    def load_all(self):
        pass

