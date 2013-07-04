__author__ = 'ajboehmler'

import os
import uuid
import pickle
import datetime
from werkzeug import secure_filename

from app import app
import models


ALLOWED_EXTENSIONS = set(['xls', 'xlsx', 'csv'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def get_excel_file_path(file_id):
    file_record = models.UploadedFile.get(models.UploadedFile.id == file_id)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_record.directory, file_record.name)
    return file_path


def save_excel_file(file, directory):
    if file and allowed_file(file.filename):
        # Create a new file record object in the database.
        file_record = models.UploadedFile()
        file_record.name = ''
        file_record.directory = directory
        file_record.created = datetime.datetime.now()
        file_record.save()

        # Store the file with the file record's ID prepended to the name.
        filename = secure_filename(str(file_record.id) + '_' + file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], directory, filename))

        # Update the file record with the file's name.
        file_record.name = filename
        file_record.save()

        return file_record

    raise Exception('The file is not valid!')


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