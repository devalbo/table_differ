__author__ = 'ajboehmler'

import zlib
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


class Baseline(db.Model):
    name = CharField()
    description = CharField()
    default_cell_comparison_type = IntegerField(choices=cell_comparisons.CHOICE_LABELS)
    td_baseline_grid_json_zipped = BlobField()
    td_table_comparison_json_zipped = BlobField()

    last_modified = DateTimeField()
    created = DateTimeField()
    adhoc = BooleanField()

    def __unicode__(self):
        return self.name

    @property
    def td_baseline_grid_json(self):
        return zlib.decompress(self.td_baseline_grid_json_zipped)

    @property
    def td_table_comparison_json(self):
        return zlib.decompress(self.td_table_comparison_json_zipped)


class ComparisonResult(db.Model):
    actual_table_csv_zipped = BlobField()
    comparison_image = BlobField()
    baseline = ForeignKeyField(Baseline)
    timestamp = DateTimeField()

    def __unicode__(self):
        return "%s comparison - performed at %s" % (
            cell_comparisons.IDS_TO_CMP_LABEL_DICT[self.baseline.default_cell_comparison_type],
            self.timestamp.strftime('%Y-%m-%d %I:%M %p'))

    @property
    def actual_table_csv(self):
        return zlib.decompress(self.actual_table_csv_zipped)
