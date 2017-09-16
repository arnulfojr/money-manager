
from flask import make_response

from .. import blueprint


@blueprint.route('/', methods=['GET'])
def hello():
    return make_response(u"Hello", 200)


@blueprint.route('/<name>/', methods=['GET'])
def hello_world(name='World'):
    """Says hello world with the given name"""
    message = u"Hello {}!".format(name)
    response = make_response(message, 200)
    return response

