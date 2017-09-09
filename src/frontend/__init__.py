
from flask import Flask


app = Flask(__name__)

# import blueprints
from hello import blueprint as hello_bp

app.register_blueprint(hello_bp)

