
from .. import blueprint


@blueprint.route('/', methods=['GET'])
def get_accounts():
    return u"accounts"

