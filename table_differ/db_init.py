__author__ = 'ajboehmler'

import os
import models
import dev_config as config
# import prod_config as config

config_obj = config.Configuration()
sqlite_file = config_obj.DATABASE['name']
if os.path.exists(sqlite_file):
    os.remove(sqlite_file)

models.User.create_table()

admin = models.User(username='admin',
                    email='admin@example.com',
                    admin=True,
                    active=True)
admin.set_password('admin')
admin.save()

models.Baseline.create_table()
models.ComparisonResult.create_table()
