import re, pickle
import json
from collections import OrderedDict
import cell_comparisons

# COMPARE_LITERAL = "Literal"
# COMPARE_RE_SKIP = "Regular Expression"
# COMPARE_PRIMARY_KEY = "Primary Key (not implemented yet)"
#
# _UPDATE_TYPES = {}
#
# def update_method(update_type_name):
#     def wrapper(func):
#         _UPDATE_TYPES[update_type_name] = func
#         return func
#     return wrapper
#
# def compare_tables(t1, t2, comparator):
#     comparison = TdComparison(t1, t2)
#     comparison.do_comparison(comparator)
#     return comparison
#
# class TdComparison:
#
#     def __init__(self, expected_table, actual_table):
#         self._expected_table = expected_table
#         self._actual_table = actual_table
#         self._diff_cells = None
#         self._same_cells = None
#         self._expected_table_only_cells = None
#         self._actual_table_only_cells = None
#         self._neither_table_cell_coords = None
#         self._comparison_notes = []
#         self._comparator = None
#
#     def do_comparison(self, comparator):
#         if comparator == COMPARE_LITERAL:
#             self._do_compare_literal()
#         elif comparator == COMPARE_RE_SKIP:
#             self._do_compare_re_skip()
#         elif comparator == COMPARE_PRIMARY_KEY:
#             pass
#         else:
#             raise Exception("No such comparator: %s" % comparator)
#
#         self._comparator = comparator
#
#     @property
#     def max_rows(self):
#         return max(self._expected_table.row_count, self._actual_table.row_count)
#
#     @property
#     def max_cols(self):
#         return max(self._expected_table.col_count, self._actual_table.col_count)
#
#     @property
#     def expected_table(self):
#         return self._expected_table
#
#     @property
#     def actual_table(self):
#         return self._actual_table
#
#     @property
#     def diff_cells(self):
#         return self._diff_cells
#
#     @property
#     def same_cells(self):
#         return self._same_cells
#
#     @property
#     def expected_table_only_cells(self):
#         return self._expected_table_only_cells
#
#     @property
#     def actual_table_only_cells(self):
#         return self._actual_table_only_cells
#
#     @property
#     def neither_table_cell_coords(self):
#         return self._neither_table_cell_coords
#
#     @property
#     def comparison_notes(self):
#         return self._comparison_notes
#
#     @property
#     def tables_equivalent(self):
#         if self._comparator is None:
#             raise Exception("No comparison performed yet")
#
#         if len(self.diff_cells) > 0:
#             return False
#         if len(self.expected_table_only_cells) > 0:
#             return False
#         if len(self.actual_table_only_cells) > 0:
#             return False
#
#         if len(self.same_cells) == 0:
#             if self.max_rows > 0 or self.max_cols > 0:
#                 return False
#
#         return True
#
#     def _do_compare_literal(self):
#         def literal_compare_func(expected_value, actual_value):
#             return expected_value.strip() == actual_value.strip()
#
#         return self._do_compare(literal_compare_func)
#
#     def _do_compare_re_skip(self):
#         def re_compare_func(expected_value, actual_value):
#             if expected_value.upper() == "<SKIP>":
#                 return True
#             rx = re.compile("^%s$" % expected_value)
#             return rx.match(actual_value) is not None
#
#         return self._do_compare(re_compare_func)
#
#     def _do_compare(self, compare_func):
#         diffs = {}
#         sames = {}
#         expected_table_only_cells = {}
#         actual_table_only_cells = {}
#         neither_table_cell_coords = []
#
#         for row_index in range(self.max_rows):
#             for col_index in range(self.max_cols):
#
#                 expected_table_cell_found = False
#                 actual_table_cell_found = False
#
#                 try:
#                     expected_table_cell_value = self._expected_table.get_value(row_index, col_index)
#                     expected_table_cell_found = True
#                 except (KeyError, IndexError):
#                     try:
#                         actual_table_only_cells[(row_index, col_index)] = self._actual_table.get_value(row_index, col_index)
#                     except (KeyError, IndexError):
#                         pass
#
#                 try:
#                     actual_table_cell_value = self._actual_table.get_value(row_index, col_index)
#                     actual_table_cell_found = True
#                 except (KeyError, IndexError):
#                     try:
#                         expected_table_only_cells[(row_index, col_index)] = self._expected_table.get_value(row_index, col_index)
#                     except (KeyError, IndexError):
#                         pass
#
#                 if expected_table_cell_found and actual_table_cell_found:
#                     if compare_func(expected_table_cell_value, actual_table_cell_value):
#                         sames[(row_index, col_index)] = expected_table_cell_value
#                     else:
#                         diffs[(row_index, col_index)] = (expected_table_cell_value, actual_table_cell_value)
#
#                 elif not expected_table_cell_found and not actual_table_cell_found:
#                     neither_table_cell_coords.append((row_index, col_index))
#
#         self._same_cells = sames
#         self._diff_cells = diffs
#         self._expected_table_only_cells = expected_table_only_cells
#         self._actual_table_only_cells = actual_table_only_cells
#         self._neither_table_cell_coords = neither_table_cell_coords
#
# def do_results_update(comparison_result, update_type, update_args):
#     update_type_method = _UPDATE_TYPES[update_type]
#     return update_type_method(comparison_result, update_args)
#
# @update_method("use_actual_in_region")
# def do_use_actual_in_region(comparison_result, update_args):
#     start_row, start_col, end_row, end_col = update_args["region"]
#     cell_indices = [(row_index, col_index)
#                     for row_index in range(start_row, end_row + 1)
#                     for col_index in range(start_col, end_col + 1)]
#     actual_table = pickle.loads(comparison_result.pickled_actual_table)
#     baseline = comparison_result.baseline
#     baseline_grid = pickle.loads(comparison_result.baseline.pickled_td_baseline_grid)
#
#     for (cell_x, cell_y) in cell_indices:
#         new_value = actual_table.get_value(cell_x, cell_y)
#         literal_comparison = cell_comparisons.LiteralCellComparison(new_value)
#         baseline_grid.set_cell_comparison(cell_x, cell_y, literal_comparison)
#
#     baseline.pickled_td_baseline_grid = pickle.dumps(baseline_grid)
#     baseline.save()
#     return (baseline, )
#
# @update_method("ignore_cells_in_region")
# def do_ignore_cells_in_region(comparison_result, update_args):
#     start_row, start_col, end_row, end_col = update_args["region"]
#     cell_indices = [(row_index, col_index)
#                     for row_index in range(start_row, end_row + 1)
#                     for col_index in range(start_col, end_col + 1)]
#
#     actual_table = pickle.loads(comparison_result.pickled_actual_table)
#     baseline = comparison_result.baseline
#     baseline_grid = pickle.loads(comparison_result.baseline.pickled_td_baseline_grid)
#
#     for (cell_x, cell_y) in cell_indices:
#         new_value = actual_table.get_value(cell_x, cell_y)
#         literal_comparison = cell_comparisons.IgnoreDifferencesComparison(new_value)
#         baseline_grid.set_cell_comparison(cell_x, cell_y, literal_comparison)
#
#     baseline.pickled_td_baseline_grid = pickle.dumps(baseline_grid)
#     baseline.save()
#     return (baseline, )
#
#
#
# _COMPARISON_OPERATIONS = OrderedDict()
#
# def comparison_operation(cls):
#     _COMPARISON_OPERATIONS[cls.comparison_name] = cls
#     return cls

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
#
#
# def make_cell_comparison_grid(cell_comparisons):
#     grid = {}
#     for cell_comparison in cell_comparisons:
#         grid_comparison_class = _COMPARISON_OPERATIONS[cell_comparison.comparison_name]
#         comparison = grid_comparison_class()
#         configuration = json.loads(cell_comparison.configuration_json)
#         for attrib, value in configuration.items():
#             setattr(comparison, attrib, value)
#         grid[(cell_comparison.pos_x, cell_comparison.pos_y)] = comparison
#
#     return grid