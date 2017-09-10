
from sqlalchemy import func
from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, DateTime, Numeric

from sqlalchemy.orm import relationship

from sqlalchemy.dialects.postgresql import UUID

from lib.db import Model
from lib.db import ModelMixin


class ExchangeRate(ModelMixin, Model):
    """Exchange ratio"""

    __tablename__ = 'exchange_rate'

    code = Column(UUID, primary_key=True, nullable=False)

    # from Currency, no backref!
    from_currency_code = Column(String(4), ForeignKey('currency.code'), nullable=False)
    from_currency = relationship('Currency')

    # to Currency, no backref!
    to_currency_code = Column(String(4), ForeignKey('currency.code'), nullable=False)
    to_currency = relationship('Currency')

    # saved created
    saved_on = Column(DateTime, server_default=func.now())

    # rate
    rate = Column(Numeric(10, 2), nullable=False)

    def to_dict(self, include_currencies=True):
        """returns the exchange rate as a dictionary"""
        rate = {
            'code': self.code,
            'rate': self.rate,
            'saved_on': self.saved_on.isoformat()
        }

        if include_currencies:
            rate['from'] = self.from_currency.to_dict()
            rate['to'] = self.to_currency.to_dict()

        return rate

