
from uuid import uuid4

from sqlalchemy import func
from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, DateTime

from sqlalchemy.orm import relationship

from lib.db import Model
from lib.db import ModelMixin
from lib.db.types import GUID


class Account(ModelMixin, Model):

    __tablename__ = 'accounts'

    # Account Code
    code = Column(GUID, primary_key=True, nullable=False, default=uuid4)

    # relate the account to a user
    user_code = Column(GUID, ForeignKey('users.code'))
    user = relationship('User', backref='accounts')

    # Name of the Account
    name = Column(String, nullable=False)

    # currency
    currency_code = Column(String(4), ForeignKey('currency.code'))
    currency = relationship('Currency', backref='accounts')

    # Registered on
    registered_on = Column(DateTime, server_default=func.now())

    schema = {
        'name': {
            'type': 'string',
            'required': True,
            'empty': False
        },
        'user': {
            'type': 'dict',
            'required': True,
            'allow_unknown': True,
            'schema': {
                'code': {
                    'type': 'string',
                    'required': True,
                    'empty': False
                }
            }
        },
        'currency': {
            'type': 'dict',
            'required': True,
            'allow_unknown': True,
            'schema': {
                'code': {
                    'required': True,
                    'type': 'string',
                    'empty': False
                }
            }
        }
    }

    @classmethod
    def from_dict(cls, json, account=None):
        if account is None:
            account = cls()

        account.name = json['name']
        account.user_code = json['user']['code']
        account.currency_code = json['currency']['code']

        return account

    def to_dict(self, include_currency=True, include_user=True):
        """returns the account as a dictionary"""
        account = {
            'code': self.code,
            'name': self.name,
            'registered_on': self.registered_on.isoformat()
        }

        if include_currency:
            account['currency'] = self.currency.to_dict()

        if include_user:
            account['user'] = self.user.to_dict()

        return account

