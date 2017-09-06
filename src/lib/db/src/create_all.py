from .. import Model
from .. import engine


def create_all():
    """Create tables for all registered models"""
    Model.metadata.create_all(bind=engine)

