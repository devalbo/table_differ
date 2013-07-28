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


def export_to_csv(t, file_location):
    pass

def create_from_csv(t):
    pass

