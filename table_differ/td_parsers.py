
#import pydataframe
import json
from xlrd import open_workbook
import td_table
import csv


def load_table_from_handson_json(handson_json):
    table_data = handson_json
    if type(table_data) is str:
        table_data = json.loads(handson_json)

    grid_data = table_data['grid_data']
    row_count = int(table_data['row_count'])
    col_count = int(table_data['col_count'])
    table_rows = [[grid_data[i + (j * col_count)]
                   for i in range(col_count)]
                  for j in range(row_count)]

    t = td_table.TdTable()
    for row in table_rows:
        t.add_row(row)

    # table_info = {"row_count": row_count,
    #               "col_count": col_count}

    #return table_info, table_rows, t
    return t

def load_table_from_xls(filename, worksheet_name=""):
    wb = open_workbook(filename)

    for s in wb.sheets():
        if s.name == worksheet_name or worksheet_name == "":
            t = td_table.TdTable()
            for row_index in range(s.nrows):
                new_row = []
                for col_index in range(s.ncols):
                    new_row.append(s.cell(row_index, col_index).value)
                t.add_row(new_row)
            return t

    raise Exception("No such worksheet found: %s" % worksheet_name)


def load_table_from_csv(filename):
    t = td_table.TdTable()
    with open(filename, 'rb') as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csvReader:
            new_row = []
            for value in row:
                new_row.append(value)
            t.add_row(new_row)
        return t


# adapted from https://code.google.com/p/pydataframe/source/browse/pydataframe/parsers.py
class DF2Excel:
    """Use xlrd and xlwt to write 'real' excel files"""

    def read(self, filename, sheet_name=None, row_offset=0, col_offset=0,
             row_max=None, col_max=None, filter_empty=False, NA_string=None,
             handle_encoding_errors=lambda u: u.encode('latin-1', 'replace').strip().decode('latin-1'),
             columns_to_include=None, keep_first_row=False):
        import xlrd
        if filename.endswith('.gz'):
            tf = tempfile.NamedTemporaryFile()
            op = _open_file(filename,'rb')
            tf.write(op.read())
            op.close()
            tf.flush()
            filename = tf.name
        else:
            tf = None
        try:
            wb = xlrd.open_workbook(filename)
            if sheet_name is None:
                ws = wb.sheet_by_index(0)
            else:
                if type(sheet_name) == int:
                    ws = wb.sheet_by_index(sheet_name)
                else:
                    ws = wb.sheet_by_name(sheet_name)
            if row_max is None:
                row_max = ws.nrows
            if col_max is None:
                col_max = ws.ncols
            cols = {}
            col_names_in_order = []
            columns_used = []
            for yy, col_name in enumerate(ws.row(0 + row_offset)[col_offset: col_max]):
                name = col_name.value
                counter = 2
                while name in col_names_in_order:
                    name = "%s_%i" % ( col_name.value, counter )
                    counter += 1
                col_names_in_order.append(name)
                if not columns_to_include or name in columns_to_include:
                    cols[name] = []
                    columns_used.append(yy)
            if not columns_used:
                raise ValueError("No columns to import - columns_to_include did not reference any present. Column_to_include was %s, available: %s" % (columns_to_include, col_names_in_order))
            if columns_to_include and set(columns_to_include).difference(col_names_in_order):
                raise ValueError("Nonexistant column name(s) in columns_to_include: %s" % (set(columns_to_include).difference(col_names_in_order),))
            for row_no in xrange(0 + row_offset + 1, row_max):
                row = ws.row(row_no)
                found = False
                for y in  columns_used:#xrange(0 + col_offset, col_max):
                    value = row[y].value
                    try:
                        if str(value).strip() == '' or row[y].ctype == xlrd.XL_CELL_EMPTY or row[y].ctype == xlrd.XL_CELL_ERROR:
                            value = None
                        if type(value) == unicode and value == NA_string:
                            value = None
                    except UnicodeEncodeError:
                        value = handle_encoding_errors(value)
                    cols[col_names_in_order[y - col_offset]].append((value))
                    if value:
                        found = True
                if not found and filter_empty:
                    for k in col_names_in_order:
                        cols[k].pop()
            return pydataframe.DataFrame(cols, [x for (yy,x) in enumerate(col_names_in_order) if yy in columns_used])
        finally:
            if tf:
                tf.close()

