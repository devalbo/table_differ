from util import table_comparison
import td_comparison

@table_comparison
class RowByRowTableComparison:
    comparison_type_id = -1  # automatically assigned at startup
    comparison_type_name = "table.compare-rowbyrow"
    comparison_label = "Row by row comparison"
    persist_attributes = []

    def compare_table_to_baseline_grid(self, actual_table, baseline_grid):
        diffs = {}
        sames = {}
        baseline_grid_only_cells = {}
        actual_table_only_cells = {}
        neither_table_cell_coords = []

        for row_index in range(max([baseline_grid.row_count, actual_table.row_count])):
            for col_index in range(max([baseline_grid.col_count, actual_table.col_count])):

                baseline_cell_found = False
                actual_table_cell_found = False

                try:
                    baseline_cell_comparison = baseline_grid.get_cell_comparison(row_index, col_index)
                    baseline_cell_found = True
                except (KeyError, IndexError):
                    try:
                        actual_table_only_cells[(row_index, col_index)] = actual_table.get_value(row_index, col_index)
                    except (KeyError, IndexError):
                        pass

                try:
                    actual_table_cell_value = actual_table.get_value(row_index, col_index)
                    actual_table_cell_found = True
                except (KeyError, IndexError):
                    try:
                        baseline_grid_only_cells[(row_index, col_index)] = baseline_grid.get_expected_value(row_index, col_index)
                    except (KeyError, IndexError):
                        pass

                if baseline_cell_found and actual_table_cell_found:
                    if baseline_cell_comparison.do_compare(actual_table_cell_value):
                        sames[(row_index, col_index)] = str(baseline_cell_comparison)
                    else:
                        diffs[(row_index, col_index)] = (str(baseline_cell_comparison), actual_table_cell_value)

                elif not baseline_cell_found and not actual_table_cell_found:
                    neither_table_cell_coords.append((row_index, col_index))

        comparison_result = td_comparison.TdComparison(baseline_grid, actual_table)
        comparison_result._same_cells = sames
        comparison_result._diff_cells = diffs
        comparison_result._expected_table_only_cells = baseline_grid_only_cells
        comparison_result._actual_table_only_cells = actual_table_only_cells
        comparison_result._neither_table_cell_coords = neither_table_cell_coords

        return comparison_result
