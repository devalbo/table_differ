__author__ = 'ajboehmler'

import datetime

from flask_peewee.auth import BaseUser  # provides password helpers..
from peewee import *

from app import db

class User(db.Model, BaseUser):
    username = CharField()
    password = CharField()
    email = CharField()
    join_date = DateTimeField(default=datetime.datetime.now)
    active = BooleanField(default=True)
    admin = BooleanField(default=False)

    def __unicode__(self):
        return self.username

class UploadedFile(db.Model):
    name = CharField()
    directory = CharField()
    created = DateTimeField()

class ComparisonType(db.Model):
    name = CharField()

    COMPARISON_TYPE_LITERAL = 'Literal'
    COMPARISON_TYPE_REGEX = 'Regular Expression'

    def __unicode__(self):
        return self.name



class Baseline(db.Model):
    name = CharField()
    file = ForeignKeyField(UploadedFile)
    comparison = ForeignKeyField(ComparisonType)

class NewBaseline(db.Model):
    name = CharField()
    baseline_table_id = CharField()
    comparison_type = ForeignKeyField(ComparisonType)

class ComparisonResult(db.Model):
    expected_table_id = CharField()
    actual_table_id = CharField()
    comparison_results_id = CharField()
    comparison_type = ForeignKeyField(ComparisonType)
    baseline = ForeignKeyField(NewBaseline)
    timestamp = DateTimeField()

    def __unicode__(self):
        return "%s comparison - performed at %s" % (self.comparison_type.name, self.timestamp)
