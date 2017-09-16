
from flask import Flask
from lib.db import setup_app


app = Flask(__name__)

setup_app(app)


# import blueprints
from accounts import blueprint as accounts_bp
from users import blueprint as users_bp
from currency import blueprint as currency_bp


# register blueprints
app.register_blueprint(accounts_bp)
app.register_blueprint(users_bp)
app.register_blueprint(currency_bp)

