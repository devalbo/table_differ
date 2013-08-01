from flask import Flask

from flask_peewee.db import Database
import reverseproxied


APP_CONFIG_NAME = "dev_config.Configuration"
try:
    import sys
    APP_CONFIG_NAME = sys.argv[1]
except IndexError:
    # no config supplied, will use dev_config by default
    pass


app = Flask(__name__)
app.config.from_object(APP_CONFIG_NAME)
app.wsgi_app = reverseproxied.ReverseProxied(app.wsgi_app)

db = Database(app)
