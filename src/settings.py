
import os


# DB settings
DB_URI = os.getenv('DB_URI')

DB_ECHO = os.getenv('DB_ECHO', 'True') == 'True'


# Application Settings
USE_RELOADER = os.getenv('USE_RELOAD', False) == 'True'

USE_DEBUGGER = os.getenv('USE_DEBUGGER', False) == 'True'

