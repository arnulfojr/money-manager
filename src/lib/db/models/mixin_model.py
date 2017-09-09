
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound

from .. import session


class ModelMixin(object):
    """
    Inherit and override in the models:

        * get
        * _query
        * _repr_
    """
    @classmethod
    def get(cls, code):
        if not hasattr(cls, 'code'):
            raise NotImplemented(
                    'This model does not have code implemented')
        query = session.query(cls)
        query = query.filter(cls.code == code)
        return query.one()

    @classmethod
    def _query(cls, order_by=None, offset=None, limit=None):
        query = session.query(cls)
        if order_by is not None:
            query = query.order_by(order_by)
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        return query

    @classmethod
    def query(cls, *args, **kwargs):
        return cls.query(*args, **kwargs).all()

    @classmethod
    def count(cls, *args, **kwargs):
        return cls._query(*args, **kwargs).count()

    @classmethod
    def first(cls, *args, **kwargs):
        return cls._query(*args, **kwargs).first()

    @classmethod
    def exists(cls, *args, **kwargs):
        try:
            cls.get(*args, **kwargs)
            return True
        except NoResultFound:
            return False
        except MultipleResultsFound:
            return True

    def __repr__(self):
        return "<{}: {}>".format(self.__class__.__name__, id(self))

