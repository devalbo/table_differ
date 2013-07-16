__author__ = 'ajboehmler'

import os
import uuid
import pickle
import datetime
from werkzeug import secure_filename

from app import app
import models


def store_comparison(comparison):
    comparison_id = uuid.uuid4()
    pickle.dump(comparison, open(os.path.join(app.config['STORAGE_LOCATION'],
                                              "compare_results",
                                              "%s.p" % comparison_id,
                                              ),
                                 "wb"))
    return comparison_id

def retrieve_comparison(comparison_id):
    comparison = pickle.load(open(os.path.join(app.config['STORAGE_LOCATION'],
                                               "compare_results",
                                               "%s.p" % comparison_id,
                                               ),
                                  "rb"))
    return comparison


def store_td_table(td_table):
    td_table_id = uuid.uuid4()
    pickle.dump(td_table, open(os.path.join(app.config['STORAGE_LOCATION'],
                                            "tables",
                                            "%s.p" % td_table_id,
                                            ),
                               "wb"))
    return td_table_id

def retrieve_td_table(td_table_id):
    td_table = pickle.load(open(os.path.join(app.config['STORAGE_LOCATION'],
                                             "tables",
                                             "%s.p" % td_table_id,
                                             ),
                                "rb"))
    return td_table
