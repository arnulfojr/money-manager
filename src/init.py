
from flask import Flask

from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple

from api import app as api_app
from frontend import app as frontend_app

from settings import USE_RELOADER, USE_DEBUGGER


application = DispatcherMiddleware(frontend_app, {
    '/api': api_app
})

if __name__ == '__main__':
    run_simple('0.0.0.0', 5000, application,
            use_reloader=USE_RELOADER, use_debugger=USE_DEBUGGER)
