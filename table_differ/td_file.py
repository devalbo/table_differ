__author__ = 'ajb'

import os, uuid
from werkzeug import secure_filename
from app import app

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
        # file_record = models.UploadedFile()
        # file_record.name = ''
        # file_record.directory = directory
        # file_record.created = datetime.datetime.now()
        # file_record.save()

        # Store the file with the file record's ID prepended to the name.
        # fid = uuid.uuid4()
        # filename = secure_filename(str(file_record.id) + '_' + file.filename)
        filename = "%s.%s" % (uuid.uuid4(), file.filename.split('.')[-1])
        filelocation = os.path.join(app.config['UPLOAD_FOLDER'], directory, filename)
        file.save(filelocation)

        return filelocation

        # Update the file record with the file's name.
        # file_record.name = filename
        # file_record.save()
        #
        # return file_record

    raise Exception('The file is not valid!')