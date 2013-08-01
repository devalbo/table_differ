__author__ = 'ajboehmler'

import os, platform

class Configuration(object):
    DATABASE = {
        'name': 'table_differ.db',
        'engine': 'peewee.SqliteDatabase',
        'check_same_thread': False,
        }
    DEBUG = True
    SECRET_KEY = 'shhhh'

# # example Postgres configuration
# class Configuration(object):
#     DATABASE = {
#     'name': 'table_differ',
#     'engine': 'peewee.PostgresqlDatabase',
#     'user': 'table_differ',
#     'password': 'table_differ',
#     }

    STORAGE_LOCATION = ""
    if platform.system().startswith("Windows"):
        STORAGE_LOCATION = 'C:\\table_differ'
    else:
        STORAGE_LOCATION = '/tmp/table_differ'

    UPLOAD_FOLDER = os.path.join(STORAGE_LOCATION, 'uploads')