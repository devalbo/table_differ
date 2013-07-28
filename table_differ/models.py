__author__ = 'ajboehmler'

import datetime
from flask_peewee.auth import BaseUser  # provides password helpers..
import cell_comparisons
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

class CellComparison(db.Model):
    comparison_name = CharField()
    configuration_json = CharField()
    x_pos = IntegerField()
    y_pos = IntegerField()


class TableComparison(db.Model):
    comparison_name = CharField()
    configuration_json = CharField()


class Baseline(db.Model):
    name = CharField()
    description = CharField()
    default_cell_comparison_type = IntegerField(choices=cell_comparisons.CHOICES)
    pickled_td_baseline_grid = BlobField()
    pickled_td_table_comparison = BlobField()

    last_modified = DateTimeField()
    created = DateTimeField()
    adhoc = BooleanField()

    def __unicode__(self):
        return self.name


class ComparisonResult(db.Model):
    pickled_actual_table = BlobField()
    pickled_comparison_report = BlobField()
    comparison_image = BlobField()
    baseline = ForeignKeyField(Baseline)
    timestamp = DateTimeField()

    def __unicode__(self):
        return "%s comparison - performed at %s" % (
            cell_comparisons.CHOICES[self.baseline.default_cell_comparison_type],
            self.timestamp)
