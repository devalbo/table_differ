__author__ = 'ajboehmler'

from flask_peewee.admin import Admin

from app import app
from auth import auth
from models import Baseline, ComparisonResult

admin = Admin(app, auth)
auth.register_admin(admin)
# or you could admin.register(User, ModelAdmin) -- you would also register
# any other models here.
admin.register(ComparisonResult)
admin.register(Baseline)