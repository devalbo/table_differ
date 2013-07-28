__author__ = 'ajboehmler'

import datetime
# import pickle
from flask_peewee.auth import BaseUser  # provides password helpers..
# import td_comparison
# import td_baseline
import cell_comparisons
from peewee import *
# from collections import OrderedDict

from app import db

# class ComparisonOperation(db.Model):
#
#     CHOICES = OrderedDict([(i, k) for i, k in enumerate(td_comparison._COMPARISON_OPERATIONS.keys())])
#     IDS_TO_CHOICES_DICT = dict([(k, i) for i, k in enumerate(td_comparison._COMPARISON_OPERATIONS.keys())])
#
#     type = IntegerField(choices=[(k, CHOICES[k]) for k in CHOICES.keys()])
#     pickled_comparison_op = BlobField()
#
#     @property
#     def name(self):
#         return self.CHOICES[self.type]
#
#     def __unicode__(self):
#         return self.CHOICES[self.type]
#
#     def __str__(self):
#         return self.CHOICES[self.type]
#
#
# def create_comparison_operation(comp_type):
#     comp_type_name = ComparisonOperation.CHOICES[comp_type]
#     comp_instance_class = td_comparison._COMPARISON_OPERATIONS[comp_type_name]
#     comp_instance = comp_instance_class()
#
#     comparison_operation = ComparisonOperation.create(
#         type=comp_type,
#         pickled_comparison_op=pickle.dumps(comp_instance),
#     )
#
#     return comparison_operation


class User(db.Model, BaseUser):
    username = CharField()
    password = CharField()
    email = CharField()
    join_date = DateTimeField(default=datetime.datetime.now)
    active = BooleanField(default=True)
    admin = BooleanField(default=False)

    def __unicode__(self):
        return self.username

# class OldBaseline(db.Model):
#     name = CharField()
#     description = CharField()
#     pickled_expected_table = BlobField()
#     comparison_operation = ForeignKeyField(ComparisonOperation)
#     last_modified = DateTimeField()
#     created = DateTimeField()
#     adhoc = BooleanField()
#
#     def __unicode__(self):
#         return self.name

# class CellComparison(db.Model):
#     CHOICES = OrderedDict([(i, k) for i, k in enumerate(cell_comparisons._CELL_COMPARISONS.keys())])
#     IDS_TO_CHOICES_DICT = dict([(k, i) for i, k in enumerate(cell_comparisons._CELL_COMPARISONS.keys())])
#
#     type = IntegerField(choices=[(k, CHOICES[k]) for k in CHOICES.keys()])
#     pickled_comparison_op = BlobField()
#
#     @property
#     def name(self):
#         return self.CHOICES[self.type]
#
#     def __unicode__(self):
#         return self.CHOICES[self.type]
#
#     def __str__(self):
#         return self.CHOICES[self.type]
#
#
# def create_comparison_operation(comp_type):
#     comp_type_name = CellComparison.CHOICES[comp_type]
#     comp_instance_class = td_comparison._COMPARISON_OPERATIONS[comp_type_name]
#     comp_instance = comp_instance_class()
#
#     comparison_operation = ComparisonOperation.create(
#         type=comp_type,
#         pickled_comparison_op=pickle.dumps(comp_instance),
#     )
#
#     return comparison_operation

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
    # jsonpickled_td_baseline_grid = TextField()
    # jsonpickled_td_table_comparison = TextField()
    # default_cell_comparison_type = IntegerField(choices=cell_comparisons.CHOICES)
    # cell_comparisons = ForeignKeyField(CellComparison)
    # table_comparison_configuration = ForeignKeyField(TableComparison)

    last_modified = DateTimeField()
    created = DateTimeField()
    adhoc = BooleanField()

    def __unicode__(self):
        return self.name



class ComparisonResult(db.Model):
    pickled_actual_table = BlobField()
    pickled_comparison_report = BlobField()
    # jsonpickled_actual_table = TextField()
    # jsonpickled_comparison_report = TextField()
    comparison_image = BlobField()
    baseline = ForeignKeyField(Baseline)
    timestamp = DateTimeField()

    def __unicode__(self):
        return "%s comparison - performed at %s" % (
            cell_comparisons.CHOICES[self.baseline.default_cell_comparison_type],
            self.timestamp)
