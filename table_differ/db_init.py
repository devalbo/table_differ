__author__ = 'ajboehmler'

import models

models.User.create_table()

admin = models.User(username='admin',
                    email='admin@example.com',
                    admin=True,
                    active=True)
admin.set_password('admin')
admin.save()

# Create the comparison settings table.
models.ComparisonSettings.create_table()

comparison_literal = models.ComparisonType(name='Literal')


models.UploadedFile.create_table()
models.Baseline.create_table()