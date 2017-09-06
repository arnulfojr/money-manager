
from .. import session


def setup_app(app):
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        session.remove()

