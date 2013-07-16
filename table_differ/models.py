__author__ = 'ajboehmler'

import datetime
import pickle
from collections import OrderedDict
from flask_peewee.auth import BaseUser  # provides password helpers..
from peewee import *

from app import db


import collections
_COMPARISON_OPERATIONS = collections.OrderedDict()

def comparison_operation(cls):
    _COMPARISON_OPERATIONS[cls.comparison_name] = cls
    return cls

@comparison_operation
class LiteralComparisonOperation:
    comparison_name = "Literal"

    def __init__(self):
        self.cells_to_ignore = []

    def ignore_cells(self, cell_coord_list):
        for cell in cell_coord_list:
            if cell not in self.cells_to_ignore:
                print "Ignoring", cell
                self.cells_to_ignore.append(cell)


@comparison_operation
class RegExComparisonOperation:
    comparison_name = "Regular Expression"

    def __init__(self):
        self.cells_to_ignore = []

    def ignore_cells(self, cell_coord_list):
        for cell in cell_coord_list:
            if cell not in self.cells_to_ignore:
                self.cells_to_ignore.append(cell)

class ComparisonOperation(db.Model):

    OPS = [(i, k) for i, k in enumerate(_COMPARISON_OPERATIONS.keys())]
    OPS_DICT = dict(choice for choice in OPS)
    CHOICES = OrderedDict(sorted(OPS_DICT.items(), key=lambda t: t[0]))

    type = IntegerField(choices=[(k, CHOICES[k]) for k in CHOICES.keys()])
    pickled_comparison_op = BlobField()

    @property
    def name(self):
        return self.CHOICES[self.type]

    def __unicode__(self):
        return self.CHOICES[self.type]

    def __str__(self):
        return self.CHOICES[self.type]

    # @property
    # def comparison_op(self):
    #     ret_val = pickle.loads(self.pickled_comparison_op)
    #     return ret_val
    #
    # @comparison_op.setter
    # def set_comparison_op(self, value):
    #     pickled_value = pickle.dumps(value)
    #     self.pickled_comparison_op = pickled_value


def create_comparison_operation(comp_type):
    comp_type_name = ComparisonOperation.CHOICES[comp_type]
    comp_instance_class = _COMPARISON_OPERATIONS[comp_type_name]
    comp_instance = comp_instance_class()

    comparison_operation = ComparisonOperation.create(
        type=comp_type,
        pickled_comparison_op=pickle.dumps(comp_instance),
    )

    return comparison_operation


class User(db.Model, BaseUser):
    username = CharField()
    password = CharField()
    email = CharField()
    join_date = DateTimeField(default=datetime.datetime.now)
    active = BooleanField(default=True)
    admin = BooleanField(default=False)

    def __unicode__(self):
        return self.username

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
    source = ForeignKeyField(BaselineSource)

    def __unicode__(self):
        return self.name

class ComparisonResult(db.Model):
    pickled_actual_table = BlobField()
    pickled_comparison_report = BlobField()
    comparison_image = BlobField()
    baseline = ForeignKeyField(Baseline)
    timestamp = DateTimeField()

    def __unicode__(self):
        return "%s comparison - performed at %s" % (self.baseline.comparison_operation, self.timestamp)
