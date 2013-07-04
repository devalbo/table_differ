__author__ = 'ajboehmler'

import models

models.User.create_table()

admin = models.User(username='admin',
                    email='admin@example.com',
                    admin=True,
                    active=True)
admin.set_password('admin')
admin.save()

models.UploadedFile.create_table()
models.Baseline.create_table()
models.NewBaseline.create_table()
models.ComparisonResult.create_table()

# Create the comparison settings table.
models.ComparisonType.create_table()

models.ComparisonType.create(name=models.ComparisonType.COMPARISON_TYPE_LITERAL)
models.ComparisonType.create(name=models.ComparisonType.COMPARISON_TYPE_REGEX)