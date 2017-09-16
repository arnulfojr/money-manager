
from flask import Flask

from lib.db import setup_app


app = Flask(__name__)

setup_app(app)


# import blueprints
from hello import blueprint as hello_bp

# register blueprints
app.register_blueprint(hello_bp)

