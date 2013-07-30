
import csv
import StringIO

class TdTable:

    def __init__(self):
        self._rows = []

    def add_row(self, row):
        self._rows.append(row)

    def get_value(self, row_index, col_index, as_str=True):
        v = self._rows[row_index][col_index]
        if as_str:
            v = unicode(v)
        return v

    def set_value(self, row_index, col_index, new_value):
        self._rows[row_index][col_index] = new_value

    @property
    def row_count(self):
        return len(self._rows)

    @property
    def col_count(self):
        return len(max(self._rows, key=len))

    @property
    def rows(self):
        return self._rows

    def to_csv_str(self):
        out_csv_str = StringIO.StringIO()
        writer = csv.writer(out_csv_str)
        for row in self.rows:
            cells = [cell for cell in row]
            writer.writerow(cells)
        to_csv = out_csv_str.getvalue()
        out_csv_str.close()
        return to_csv

def create_from_csv(csv_str):
    in_csv_str = StringIO.StringIO(csv_str)
    t = TdTable()
    for row in csv.reader(in_csv_str):
        t.add_row(row)
    return t
