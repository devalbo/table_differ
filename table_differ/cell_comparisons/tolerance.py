from util import cell_comparison

@cell_comparison
class NumberToleranceCellComparison:
    comparison_type_id = -1  # automatically assigned at startup
    comparison_type_name = "cell.compare-tolerance"
    comparison_css_class = "compare-tolerance"
    comparison_label = "Numeric Comparison w/ Tolerance"
    persist_attributes = ["baseline_value", "tolerance"]

    def __init__(self, baseline_value, tolerance=0.5):
        self.baseline_value = baseline_value
        self.tolerance = abs(tolerance)

    def do_compare(self, cmp_value):
        return self.baseline_value - self.tolerance <= cmp_value <= self.baseline_value + self.tolerance
