
from sqlalchemy import func, Column
from sqlalchemy import String, DateTime

from lib.db import Model
from lib.db import ModelMixin


class Currency(ModelMixin, Model):
    """
    Currency has relationships with:

        * Account, through accounts
    """

    __tablename__ = 'currency'

    # Currency Code -> MXN
    code = Column(String(4), primary_key=True, nullable=False)

    # Name
    name = Column(String, nullable=True)

    # registered on
    registered_on = Column(DateTime, server_default=func.now())

    schema = {
        'code': {
            'type': 'string',
            'required': True
        },
        'name': {
            'type': 'string',
            'required': False
        }
    }

    def to_dict(self):
        """returns the currency as a dictionary"""
        currency = {
            'code': self.code,
            'name': self.name,
            'registered_on': self.registered_on.isoformat()
        }

        return currency

