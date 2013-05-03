class TdTable:

    def __init__(self):
        self._rows = []

    def add_row(self, row):
        self._rows.append(row)

    def get_value(self, row_index, col_index, as_str=True):
        v = self._rows[row_index][col_index]
        if as_str:
            v = str(v)
        return v

