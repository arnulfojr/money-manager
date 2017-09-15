
from uuid import uuid4

from sqlalchemy import func, Column
from sqlalchemy import String, DateTime
from sqlalchemy.orm import relationship

from lib.db.types import GUID

from lib.db import Model
from lib.db import ModelMixin


class User(ModelMixin, Model):
    """
    Has relationship to:

        * Account through accounts
    """

    __tablename__ = 'user'

    # User code
    code = Column(GUID, primary_key=True, nullable=False, default=uuid4)

    # username
    username = Column(String(255), nullable=False, unique=True)

    # password
    password = Column(String(255), nullable=False)

    # user's first name
    first_name = Column(String(255), nullable=False)

    # user's last name
    last_name = Column(String(255), nullable=False)

    # registered on
    registered_on = Column(DateTime, server_default=func.now())

    schema = {
        'username': {
            'type': 'string',
            'required': True
        },
        'password': {
            'type': 'string',
            'required': True
        },
        'first_name': {
            'type': 'string',
            'required': True
        },
        'last_name': {
            'type': 'string',
            'required': True
        }
    }

    @classmethod
    def from_dict(cls, json, user=None):
        """
        Returns a User from a json/dictionary
        """
        if user is None:
            user = cls()

        user.username = json['username']
        user.first_name = json['first_name']
        user.last_name = json['last_name']

        user.password = json['password']

        return user

    def to_dict(self, include_pwd=False):
        """returns the user as a dictionary"""

        user_dict = {
            'code': self.code,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'registered_on': self.registered_on.isoformat()
        }

        if include_pwd:
            user_dict['password'] = self.password

        return user_dict

