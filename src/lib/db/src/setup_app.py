
from .. import session


def setup_app(app):
    """Set up the application"""
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        session.remove()

