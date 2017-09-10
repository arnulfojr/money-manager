
from sqlalchemy import func
from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, DateTime

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship

from lib.db import Model
from lib.db import ModelMixin


class Account(ModelMixin, Model):

    __tablename__ = 'accounts'

    # Account Code
    code = Column(UUID, primary_key=True, nullable=True)

    # relate the account to a user
    user_code = Column(UUID, ForeignKey('user.code'))
    user = relationship('User', backref='accounts')

    # Name of the Account
    name = Column(String, nullable=False)

    # currency
    currency_id = Column(String(4), ForeignKey('currency.code'))
    currency = relationship('Currency', backref='accounts')

    # Registered on
    registered_on = Column(DateTime, server_default=func.now())

    schema = {
        'name': {
            'type': 'string',
            'required': True
        },
        'currency': {
            'type': 'dict',
            'required': True,
            'allow_unknown': True,
            'schema': {
                'code': {
                    'required': True
                }
            }
        }
    }

    def to_dict(self, include_currency=True):
        """returns the account as a dictionary"""
        account = {
            'code': self.code,
            'name': self.name,
            'registered_on': self.registered_on.isoformat()
        }

        if include_currency:
            account['currency'] = self.currency.to_dict()

        return account

