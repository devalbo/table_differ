from flask import Flask

from flask_peewee.db import Database
import reverseproxied

app = Flask(__name__)
app.config.from_object('config.Configuration')
app.wsgi_app = reverseproxied.ReverseProxied(app.wsgi_app)

db = Database(app)



import cell_comparisons
app.jinja_env.filters['css_for_comparison_type'] = cell_comparisons.css_for_comparison_type
app.jinja_env.filters['name_for_comparison_type'] = cell_comparisons.name_for_comparison_type
