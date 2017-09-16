
from functools import wraps

from flask import request, abort


def is_json(fn):
    """Validates the request, else abort with a 400 status

    Usage:

    @app.route('/', methods=['POST'])
    @is_json
    def controller_handle():
        pass
    """
    @wraps(fn)
    def _wrap(*args, **kwargs):
        if not request.is_json:
            abort(400)
        return fn(*args, **kwargs)
    return _wrap

