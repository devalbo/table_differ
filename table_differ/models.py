__author__ = 'ajboehmler'

import datetime
import pickle
from collections import OrderedDict
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

class ComparisonOperation(db.Model):

    CHOICES_DICT = {0: "Literal",
                    1: "Regular Expression",
                    }
    # CHOICES = (OrderedDict(sorted(CHOICES_DICT.items(), key=lambda t: t[0])))
    CHOICES = OrderedDict(sorted(CHOICES_DICT.items(), key=lambda t: t[0]))

    type = IntegerField(choices=[(k, CHOICES[k]) for k in CHOICES.keys()])

    @property
    def name(self):
        return self.CHOICES[self.type]

    def __unicode__(self):
        return self.CHOICES[self.type]

    def __str__(self):
        return self.CHOICES[self.type]

class BaselineSource(db.Model):
    adhoc = BooleanField()
    description = CharField()

    def __unicode(self):
        return self.description

class Baseline(db.Model):
    name = CharField()
    pickled_expected_table = BlobField()
    comparison_operation = ForeignKeyField(ComparisonOperation)
    last_modified = DateTimeField()
    created = DateTimeField()
    source = ForeignKeyField(BaselineSource, related_name="bs_baseline")

    def __unicode__(self):
        return self.name

class ComparisonResult(db.Model):
    pickled_actual_table = BlobField()
    pickled_comparison_report = BlobField()
    comparison_image = BlobField()
    baseline = ForeignKeyField(Baseline, cascade=True)
    timestamp = DateTimeField()

    # @property
    # def actual_table(self):
    #     return pickle.loads(self.actual_table)
    #
    # @actual_table.setter
    # def actual_table(self, value):
    #     self.actual_table = pickle.dumps(value)
    #
    # @property
    # def comparison_report(self):
    #     return pickle.loads(self.comparison_report)
    #
    # @comparison_report.setter
    # def comparison_report(self, value):
    #     self.comparison_report = pickle.dumps(value)
    #
    # @property
    # def comparison_image(self):
    #     return pickle.loads(self.comparison_image)
    #
    # @comparison_image.setter
    # def comparison_image_blob(self, value):
    #     self.comparison_image = pickle.dumps(value)

    def __unicode__(self):
        return "%s comparison - performed at %s" % (self.baseline.comparison_operation, self.timestamp)

    # def delete_instance(self, recursive=False, delete_nullable=False):
    #     print "Deleting comparison result!", recursive
    #     return super(ComparisonResult, self).delete_instance(recursive, delete_nullable)