__author__ = 'ajboehmler'

import os
import models, config

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

# models.UploadedFile.create_table()
models.Baseline.create_table()
# models.OldBaseline.create_table()
models.ComparisonResult.create_table()
# models.CellComparison.create_table()
# models.TableComparison.create_table()
# models.ActualTable.create_table()
# models.ExpectedTable.create_table()
# models.ComparisonReport.create_table()
# models.ComparisonImage.create_table()

# Create the comparison settings table.
# models.ComparisonOperation.create_table()
# models.ComparisonType.create(name=models.ComparisonType.COMPARISON_TYPE_LITERAL)
# models.ComparisonType.create(name=models.ComparisonType.COMPARISON_TYPE_REGEX)
# models.CellComparison.create_table()
