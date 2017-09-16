
from flask import Blueprint


blueprint = Blueprint('account', __name__, url_prefix='/accounts')


# import controllers
from controllers import accounts

