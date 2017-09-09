
from .. import blueprint


@blueprint.route('/', methods=['GET'])
def hello():
    return u"Hello!"


@blueprint.route('/<name>/', methods=['GET'])
def hello_world(name='World'):
    return u"Hello {}!".format(name)

