from flask import Flask

from flask_peewee.db import Database
import reverseproxied

app = Flask(__name__)
app.config.from_object('config.Configuration')
app.wsgi_app = reverseproxied.ReverseProxied(app.wsgi_app)

db = Database(app)

