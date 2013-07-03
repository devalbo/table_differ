import unicodedata
class TdTable:

    def __init__(self):
        self._rows = []

    def add_row(self, row):
        self._rows.append(row)

    def get_value(self, row_index, col_index, as_str=True):
        v = self._rows[row_index][col_index]
        if as_str:
<<<<<<< HEAD
            v = unicode(v)
=======
            v = unicodedata.normalize('NFKD', unicode(v)).encode('ascii', 'ignore')
>>>>>>> ef3fe337d89f49305b59c6ab96559571be4f4314
        return v

    @property
    def row_count(self):
        return len(self._rows)

    @property
    def col_count(self):
        return len(max(self._rows, key=len))

    @property
    def rows(self):
        return self._rows

