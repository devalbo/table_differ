from mmap import mmap, ACCESS_READ
from xlrd import open_workbook
import pydataframe

##print open_workbook('data.xls')
##
##with open('data.xls','rb') as f:
##    print open_workbook(file_contents=mmap(f.fileno(),0,access=ACCESS_READ))
##    aString = open('data.xls','rb').read()
##    print open_workbook(file_contents=aString)


wb = open_workbook('data.xls')
for s in wb.sheets():
    print 'Sheet:',s.name
    for row in range(s.nrows):
        values = []
        for col in range(s.ncols):
            values.append(s.cell(row,col).value)
        print ','.join(values)
    print

p = pydataframe.parsers.DF2Excel()
d = p.read("data.xls")
print d
