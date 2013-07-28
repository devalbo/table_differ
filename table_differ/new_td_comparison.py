import pickle

COMPARE_LITERAL = "Literal"
COMPARE_RE_SKIP = "Regular Expression"
COMPARE_PRIMARY_KEY = "Primary Key (not implemented yet)"

class TdComparison:

    def __init__(self, baseline_grid, actual_table):
        self._baseline_grid = baseline_grid
        self._actual_table = actual_table
        self._diff_cells = None
        self._same_cells = None
        self._expected_table_only_cells = None
        self._actual_table_only_cells = None
        self._neither_table_cell_coords = None
        self._comparison_notes = []
        self._comparator = None

    @property
    def max_rows(self):
        return max(self._baseline_grid.row_count, self._actual_table.row_count)

    @property
    def max_cols(self):
        return max(self._baseline_grid.col_count, self._actual_table.col_count)

    @property
    def baseline_grid(self):
        return self._baseline_grid

    @property
    def actual_table(self):
        return self._actual_table

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
    def comparison_notes(self):
        return self._comparison_notes

    @property
    def tables_equivalent(self):
        # if self._comparator is None:
        #     raise Exception("No comparison performed yet")

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
    actual_table = pickle.loads(comparison_result.pickled_actual_table)
    baseline = comparison_result.baseline
    expected_table = pickle.loads(comparison_result.baseline.pickled_expected_table)

    for (cell_x, cell_y) in cell_indices:
        new_value = actual_table.get_value(cell_x, cell_y)
        expected_table.set_value(cell_x, cell_y, new_value)

    baseline.pickled_expected_table = pickle.dumps(expected_table)
    return (baseline, )

@update_method("ignore_cells_in_region")
def do_ignore_cells_in_region(comparison_result, update_args):
    start_row, start_col, end_row, end_col = update_args["region"]
    cell_indices = [(row_index, col_index)
                    for row_index in range(start_row, end_row + 1)
                    for col_index in range(start_col, end_col + 1)]

    comparison_op = pickle.loads(comparison_result.baseline.comparison_operation.pickled_comparison_op)
    comparison_op.ignore_cells(cell_indices)
    comparison_result.baseline.comparison_operation.pickled_comparison_op = pickle.dumps(comparison_op)

    return (comparison_result.baseline.comparison_operation, )


# _COMPARISON_OPERATIONS = OrderedDict()
#
# def comparison_operation(cls):
#     _COMPARISON_OPERATIONS[cls.comparison_name] = cls
#     return cls
#
# @comparison_operation
# class LiteralComparisonOperation:
#     comparison_name = "Literal"
#
#     def __init__(self):
#         self.cells_to_ignore = []
#
#     def ignore_cells(self, cell_coord_list):
#         for cell in cell_coord_list:
#             if cell not in self.cells_to_ignore:
#                 self.cells_to_ignore.append(cell)
#
#
# @comparison_operation
# class RegExComparisonOperation:
#     comparison_name = "Regular Expression"
#
#     def __init__(self):
#         self.cells_to_ignore = []
#
#     def ignore_cells(self, cell_coord_list):
#         for cell in cell_coord_list:
#             if cell not in self.cells_to_ignore:
#                 self.cells_to_ignore.append(cell)
#
#
# @comparison_operation
# class PrimaryKeyComparisonOperation:
#     comparison_name = "Primary Key (not implemented yet)"
#
#     def __init__(self):
#         self.key_column_indexes = []
#         self.cells_to_ignore = []
#
#     def ignore_cells(self, cell_coord_list):
#         for cell in cell_coord_list:
#             if cell not in self.cells_to_ignore:
#                 self.cells_to_ignore.append(cell)