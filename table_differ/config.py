__author__ = 'ajboehmler'

class Configuration(object):
    DATABASE = {
        'name': 'table_differ.db',
        'engine': 'peewee.SqliteDatabase',
        'check_same_thread': False,
        }
    DEBUG = True
    SECRET_KEY = 'shhhh'