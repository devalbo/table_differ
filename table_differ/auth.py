__author__ = 'ajboehmler'

from flask_peewee.auth import Auth  # Login/logout views, etc.

from app import app, db
from models import User

auth = Auth(app, db, user_model=User)