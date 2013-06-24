__author__ = 'ajboehmler'

from flask import render_template  # ...etc , redirect, request, url_for

from app import app
from auth import auth
from models import User


@app.route('/')
def homepage():
    return render_template('foo.html')

@app.route('/private/')
@auth.login_required
def private_view():
    # ...
    user = auth.get_logged_in_user()
    #return render_tempate(...)
    return "private"