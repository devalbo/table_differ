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

class Baseline(db.Model):
    name = CharField()
    file = ForeignKeyField(UploadedFile)
    comparison = ForeignKeyField(ComparisonType)