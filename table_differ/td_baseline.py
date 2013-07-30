
import json
import cell_comparisons

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

    def to_json(self):
        jsonable_rows = []
        for row in self.rows:
            jsonable_row = []
            for cell in row:
                jsonable_cell = cell_comparisons.get_json_dict_for_comparison(cell)
                jsonable_row.append(jsonable_cell)
            jsonable_rows.append(jsonable_row)

        return json.dumps(jsonable_rows)


def make_baseline_grid_from_json(grid_json):
    json_rows = json.loads(grid_json)
    grid = TdBaselineGrid()
    for row in json_rows:
        grid_row = []
        for cell in row:
            grid_row.append(cell_comparisons.create_comparison_from_json_dict(cell))
        grid.add_row(grid_row)
    return grid


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


def do_baseline_update(comparison_result, update_type, update_args):
    update_type_method = _UPDATE_TYPES[update_type]
    return update_type_method(comparison_result, update_args)

@update_method("ignore_cells_in_region")
def do_ignore_cells_in_region(baseline, update_args):
    start_row, start_col, end_row, end_col = update_args["region"]
    cell_indices = [(row_index, col_index)
                    for row_index in range(start_row, end_row + 1)
                    for col_index in range(start_col, end_col + 1)]

    baseline_grid = make_baseline_grid_from_json(baseline.td_baseline_grid_json)

    for (cell_x, cell_y) in cell_indices:
        new_value = unicode(baseline_grid.get_cell_comparison(cell_x, cell_y))
        new_cell_comparison = cell_comparisons.IgnoreDifferencesComparison(new_value)
        baseline_grid.set_cell_comparison(cell_x, cell_y, new_cell_comparison)

    baseline.td_baseline_grid_json = baseline_grid.to_json()
    return (baseline, )

@update_method("literal_compare_cells_in_region")
def do_literal_compare_cells_in_region(baseline, update_args):
    start_row, start_col, end_row, end_col = update_args["region"]
    cell_indices = [(row_index, col_index)
                    for row_index in range(start_row, end_row + 1)
                    for col_index in range(start_col, end_col + 1)]

    baseline_grid = make_baseline_grid_from_json(baseline.td_baseline_grid_json)

    for (cell_x, cell_y) in cell_indices:
        new_value = unicode(baseline_grid.get_cell_comparison(cell_x, cell_y))
        new_cell_comparison = cell_comparisons.LiteralCellComparison(new_value)
        baseline_grid.set_cell_comparison(cell_x, cell_y, new_cell_comparison)

    baseline.td_baseline_grid_json = baseline_grid.to_json()
    return (baseline, )

@update_method("regex_compare_cells_in_region")
def do_regex_compare_cells_in_region(baseline, update_args):
    start_row, start_col, end_row, end_col = update_args["region"]
    cell_indices = [(row_index, col_index)
                    for row_index in range(start_row, end_row + 1)
                    for col_index in range(start_col, end_col + 1)]

    baseline_grid = make_baseline_grid_from_json(baseline.td_baseline_grid_json)

    for (cell_x, cell_y) in cell_indices:
        new_value = unicode(baseline_grid.get_cell_comparison(cell_x, cell_y))
        new_cell_comparison = cell_comparisons.RegExCellComparison(new_value)
        baseline_grid.set_cell_comparison(cell_x, cell_y, new_cell_comparison)

    baseline.td_baseline_grid_json = baseline_grid.to_json()
    return (baseline, )

