
import pickle
import cell_comparisons

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


_UPDATE_TYPES = {}

def update_method(update_type_name):
    def wrapper(func):
        _UPDATE_TYPES[update_type_name] = func
        return func
    return wrapper

def do_baseline_update(comparison_result, update_type, update_args):
    update_type_method = _UPDATE_TYPES[update_type]
    return update_type_method(comparison_result, update_args)

@update_method("ignore_cells_in_region")
def do_ignore_cells_in_region(baseline, update_args):
    start_row, start_col, end_row, end_col = update_args["region"]
    cell_indices = [(row_index, col_index)
                    for row_index in range(start_row, end_row + 1)
                    for col_index in range(start_col, end_col + 1)]

    baseline_grid = pickle.loads(baseline.pickled_td_baseline_grid)

    for (cell_x, cell_y) in cell_indices:
        new_value = unicode(baseline_grid.get_cell_comparison(cell_x, cell_y))
        new_cell_comparison = cell_comparisons.IgnoreDifferencesComparison(new_value)
        baseline_grid.set_cell_comparison(cell_x, cell_y, new_cell_comparison)

    baseline.pickled_td_baseline_grid = pickle.dumps(baseline_grid)
    return (baseline, )
