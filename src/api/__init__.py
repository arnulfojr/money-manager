
from flask import Flask


app = Flask(__name__)

# import blueprints
from accounts import blueprint as accounts_bp
from users import blueprint as users_bp


# register blueprints
app.register_blueprint(accounts_bp)
app.register_blueprint(users_bp)

