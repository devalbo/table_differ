from util import table_comparison


@table_comparison
class PrimaryKeyTableComparison:
    comparison_type_id = -1  # automatically assigned at startup
    comparison_type_name = "table.compare-foreignkey"
    comparison_label = "Foreign key comparison"
    persist_attributes = []

    def compare_baseline_grid_to_table(self, actual_table, baseline_grid):
        pass
