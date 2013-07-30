import td_baseline, td_table
import cell_comparisons, table_comparisons

class TdComparison:

    def __init__(self, baseline_grid, actual_table):
        self._baseline_grid = baseline_grid
        self._actual_table = actual_table
        self._diff_cells = None
        self._same_cells = None
        self._expected_table_only_cells = None
        self._actual_table_only_cells = None
        self._neither_table_cell_coords = None

    @property
    def max_rows(self):
        return max(self._baseline_grid.row_count, self._actual_table.row_count)

    @property
    def max_cols(self):
        return max(self._baseline_grid.col_count, self._actual_table.col_count)

    @property
    def baseline_grid_row_count(self):
        return self._baseline_grid_row_count

    @property
    def baseline_grid_col_count(self):
        return self._baseline_grid_col_count

    @property
    def actual_table_row_count(self):
        return self._actual_table_row_count

    @property
    def actual_table_col_count(self):
        return self._actual_table_col_count

    @property
    def diff_cells(self):
        return self._diff_cells

    @property
    def same_cells(self):
        return self._same_cells

    @property
    def expected_table_only_cells(self):
        return self._expected_table_only_cells

    @property
    def actual_table_only_cells(self):
        return self._actual_table_only_cells

    @property
    def neither_table_cell_coords(self):
        return self._neither_table_cell_coords

    @property
    def tables_equivalent(self):
        if len(self.diff_cells) > 0:
            return False
        if len(self.expected_table_only_cells) > 0:
            return False
        if len(self.actual_table_only_cells) > 0:
            return False

        if len(self.same_cells) == 0:
            if self.max_rows > 0 or self.max_cols > 0:
                return False

        return True


def make_comparison_report(comparison_result):
    baseline_grid = td_baseline.make_baseline_grid_from_json(comparison_result.baseline.td_baseline_grid_json)
    actual_table = td_table.create_from_csv(comparison_result.actual_table_csv)
    table_comparison = table_comparisons.create_comparison_from_json(comparison_result.baseline.td_table_comparison_json)

    comparison = table_comparison.compare_table_to_baseline_grid(actual_table,
                                                                 baseline_grid)
    return comparison


_UPDATE_TYPES = {}

def update_method(update_type_name):
    def wrapper(func):
        _UPDATE_TYPES[update_type_name] = func
        return func
    return wrapper


def do_results_update(comparison_result, update_type, update_args):
    update_type_method = _UPDATE_TYPES[update_type]
    return update_type_method(comparison_result, update_args)

@update_method("use_actual_in_region")
def do_use_actual_in_region(comparison_result, update_args):
    start_row, start_col, end_row, end_col = update_args["region"]
    cell_indices = [(row_index, col_index)
                    for row_index in range(start_row, end_row + 1)
                    for col_index in range(start_col, end_col + 1)]
    actual_table = td_table.create_from_csv(comparison_result.actual_table_csv)
    baseline = comparison_result.baseline
    baseline_grid = td_baseline.make_baseline_grid_from_json(comparison_result.baseline.td_baseline_grid_json)


    for (cell_x, cell_y) in cell_indices:
        new_value = actual_table.get_value(cell_x, cell_y)
        new_cell_comparison = cell_comparisons.LiteralCellComparison(new_value)
        baseline_grid.set_cell_comparison(cell_x, cell_y, new_cell_comparison)

    baseline.td_baseline_grid_json = baseline_grid.to_json()
    return (baseline, )

@update_method("ignore_cells_in_region")
def do_ignore_cells_in_region(comparison_result, update_args):
    start_row, start_col, end_row, end_col = update_args["region"]
    cell_indices = [(row_index, col_index)
                    for row_index in range(start_row, end_row + 1)
                    for col_index in range(start_col, end_col + 1)]

    baseline = comparison_result.baseline
    baseline_grid = td_baseline.make_baseline_grid_from_json(baseline.td_baseline_grid_json)


    for (cell_x, cell_y) in cell_indices:
        new_value = unicode(baseline_grid.get_cell_comparison(cell_x, cell_y))
        new_cell_comparison = cell_comparisons.IgnoreDifferencesComparison(new_value)
        baseline_grid.set_cell_comparison(cell_x, cell_y, new_cell_comparison)

    baseline.td_baseline_grid_json = baseline_grid.to_json()
    return (baseline, )
