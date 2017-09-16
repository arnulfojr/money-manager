
from flask import Blueprint


blueprint = Blueprint('users', __name__, url_prefix='/users')


# import controllers
from controllers import users

