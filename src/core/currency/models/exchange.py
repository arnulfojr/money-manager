
from uuid import uuid4

from sqlalchemy import func
from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, DateTime, Numeric

from sqlalchemy.orm import relationship

from lib.db import session
from lib.db import Model
from lib.db import ModelMixin
from lib.db.types import GUID


class ExchangeRate(ModelMixin, Model):
    """Exchange ratio"""

    __tablename__ = 'exchange_rate'

    code = Column(GUID, primary_key=True, nullable=False, default=uuid4)

    # foreign keys
    from_currency_code = Column(String(4), ForeignKey('currency.code'), nullable=False)
    to_currency_code = Column(String(4), ForeignKey('currency.code'), nullable=False)

    # from Currency, no backref!
    from_currency = relationship('Currency', lazy='select', foreign_keys=[from_currency_code])

    # to Currency, no backref!
    to_currency = relationship('Currency', lazy='select', foreign_keys=[to_currency_code])

    # saved created
    saved_on = Column(DateTime, server_default=func.now())

    # rate
    rate = Column(Numeric(10, 2), nullable=False)

    schema = {
        'from': {
            'allow_unknown': True,
            'required': False,
            'type': 'dict',
            'schema': {
                'code': {
                    'required': True,
                    'empty': False,
                    'type': 'string'
                }
            }
        },
        'to': {
            'allow_unknown': True,
            'required': True,
            'type': 'dict',
            'schema': {
                'code': {
                    'type': 'string',
                    'required': True,
                    'empty': False
                }
            }
        },
        'rate': {
            'type': 'float',
            'required': True,
            'empty': False
        }
    }

    @classmethod
    def _rate_conversion_query(cls, for_code, from_code):
        query = session.query(cls). \
                filter(ExchangeRate.from_currency_code == from_code). \
                filter(ExchangeRate.to_currency_code == for_code)

        query = query.order_by(ExchangeRate.saved_on.desc())

        return query


    @classmethod
    def latest(cls, from_code, to_code):
        """Returns the latest rate conversion"""
        query = cls._rate_conversion_query(for_code=to_code, from_code=from_code)

        return query.first()

    @classmethod
    def history(cls, from_code, to_code):
        """Returns all the rate conversions saved for the passed currencies"""
        query = cls._rate_conversion_query(for_code=to_code, from_code=from_code)

        return query.all()

    @classmethod
    def from_dict(cls, json, rate=None, from_code=None):
        """Loads an ExchangeRate instance from a dictionary

        from_code overrides the from.code in the dictionary passed

        """
        if rate is None:
            rate = cls()

        if 'from' in json:
            rate.from_currency_code = json['from']['code']
        if from_code is not None:
            rate.from_currency_code = from_code

        rate.rate = json['rate']

        rate.to_currency_code = json['to']['code']

        return rate

    def to_dict(self, include_currencies=True):
        """returns the exchange rate as a dictionary"""
        rate = {
            'code': self.code,
            'rate': str(self.rate),
            'saved_on': self.saved_on.isoformat()
        }

        if include_currencies:
            rate['from'] = self.from_currency.to_dict()
            rate['to'] = self.to_currency.to_dict()

        return rate

