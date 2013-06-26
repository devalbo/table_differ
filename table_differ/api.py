__author__ = 'ajboehmler'

from flask_peewee.rest import RestAPI, RestResource, UserAuthentication

from app import app
from auth import auth
from models import User

user_auth = UserAuthentication(auth)

# instantiate our api wrapper and tell it to use HTTP basic auth using
# the same credentials as our auth system.  If you prefer this could
# instead be a key-based auth, or god forbid some open auth protocol.
api = RestAPI(app, default_auth=user_auth)


class UserResource(RestResource):
    exclude = ('password', 'email',)

# register our models so they are exposed via /api/<model>/
api.register(User, UserResource, auth=user_auth)