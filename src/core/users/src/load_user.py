
from functools import wraps

from .. import User


def load_user(fn):
    """Loads the user"""
    @wraps(fn)
    def _wrapper(*args, **kwargs):
        user_code = kwargs.get('user_code', None)
        user = None

        if user_code is not None:
            user = User.get(user_code)

        return fn(user=user, *args, **kwargs)

    return _wrapper

