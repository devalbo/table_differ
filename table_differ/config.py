__author__ = 'ajboehmler'

import platform, os

class Configuration(object):
    DATABASE = {
        'name': 'table_differ.db',
        'engine': 'peewee.SqliteDatabase',
        'check_same_thread': False,
        }
    DEBUG = True
    SECRET_KEY = 'shhhh'

    STORAGE_LOCATION = ""
    if platform.system().startswith("Windows"):
        STORAGE_LOCATION = 'C:\\table_differ'
    else:
        STORAGE_LOCATION = '/tmp/table_differ'

    UPLOAD_FOLDER = os.path.join(STORAGE_LOCATION, 'uploads')