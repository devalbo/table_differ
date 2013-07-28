
def make_baseline_grid_from_table(expected_table, cell_comparison_class):
    baseline_grid = TdBaselineGrid()
    for row in expected_table.rows:
        cmp_row = []
        for cell in row:
            cmp = cell_comparison_class(cell)
            cmp_row.append(cmp)
        baseline_grid.add_row(cmp_row)

    return baseline_grid

_UPDATE_TYPES = {}

def update_method(update_type_name):
    def wrapper(func):
        _UPDATE_TYPES[update_type_name] = func
        return func
    return wrapper


class TdBaselineGrid:

    def __init__(self):
        self._rows = []

    def add_row(self, row):
        self._rows.append(row)

    def get_expected_value(self, row_index, col_index):
        return self._rows[row_index][col_index]

    def get_cell_comparison(self, row_index, col_index):
        return self._rows[row_index][col_index]

    def set_cell_comparison(self, row_index, col_index, comparison):
        self._rows[row_index][col_index] = comparison

    @property
    def row_count(self):
        return len(self._rows)

    @property
    def col_count(self):
        return len(max(self._rows, key=len))

    @property
    def rows(self):
        return self._rows
