__author__ = 'ajboehmler'

import os
import uuid
import pickle
from app import app

def store_results(table1, table2, diffs, sames):
    t1_info = {"row_count": table1.row_count,
               "col_count": table1.col_count}
    t2_info = {"row_count": table2.row_count,
               "col_count": table2.col_count}

    results = {"t1_info": t1_info,
               "t2_info": t2_info,
               "diffs": diffs,
               "sames": sames}

    results_id = uuid.uuid4()
    pickle.dump(results, open(os.path.join(app.config['STORAGE_LOCATION'],
                                           "compare_results",
                                           "%s.p" % results_id),
                              "wb"))
    return results_id


def retrieve_results(results_id):
    results = pickle.load(open(os.path.join(app.config['STORAGE_LOCATION'],
                                            "compare_results",
                                            "%s.p" % results_id),
                               "rb"))
    return results

def store_new_comparison(comparison):
    comparison_id = uuid.uuid4()
    pickle.dump(comparison, open(os.path.join(app.config['STORAGE_LOCATION'],
                                              "compare_results",
                                              "%s.p" % comparison_id,
                                              ),
                                 "wb"))
    return comparison_id

def retrieve_new_comparison(comparison_id):
    comparison = pickle.load(open(os.path.join(app.config['STORAGE_LOCATION'],
                                               "compare_results",
                                               "%s.p" % comparison_id,
                                               ),
                                  "rb"))
    return comparison
