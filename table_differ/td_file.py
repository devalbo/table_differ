__author__ = 'ajb'

import os, uuid
from werkzeug import secure_filename
from app import app
import td_parsers

ALLOWED_EXTENSIONS = set(['xls', 'xlsx', 'csv'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def save_upload_file(request_file):
    if request_file and allowed_file(request_file.filename):
        filename = "%s.%s" % (uuid.uuid4(), request_file.filename.rsplit('.', 1)[1])
        filelocation = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        request_file.save(filelocation)

        return filelocation

    raise Exception('The file is not valid!')


def get_parser_for_file(file_location):
    extension = file_location.rsplit(".", 1)[1]
    if extension.lower() == "csv":
        return td_parsers.load_table_from_csv
    elif extension.lower() == "xls":
        return td_parsers.load_table_from_xls
    elif extension.lower() == "xlsx":
        return td_parsers.load_table_from_xls
    else:
        return None


def load_table_from_file_upload(request_file):
    file_location = save_upload_file(request_file)
    parser = get_parser_for_file(file_location)
    t = parser(file_location)
    return t