__author__ = 'ajboehmler'

from flask_peewee.admin import Admin, ModelAdmin

from app import app, db
from auth import auth
from models import *  #User, ComparisonOperation, Baseline, BaselineSource, ComparisonResult, Table, ComparisonReport

admin = Admin(app, auth)
auth.register_admin(admin)
# or you could admin.register(User, ModelAdmin) -- you would also register
# any other models here.
# admin.register(ComparisonOperation)
# admin.register(CellComparison)
admin.register(ComparisonResult)
# admin.register(OldBaseline)
admin.register(Baseline)
# admin.register(ActualTable)
# admin.register(ExpectedTable)
# admin.register(ComparisonReport)