__author__ = 'ajboehmler'

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
