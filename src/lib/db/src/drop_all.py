
from .. import Model
from .. import engine


def drop_all():
    """Drops all the registered models"""
    Model.metadata.drop_all(engine)
