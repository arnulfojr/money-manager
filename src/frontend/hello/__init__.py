
from flask import Blueprint


blueprint = Blueprint('frontend', __name__, url_prefix='/hello')


# import controllers
from controllers import hello

