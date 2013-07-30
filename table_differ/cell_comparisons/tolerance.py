from util import cell_comparison

@cell_comparison
class NumberToleranceCellComparison:
    comparison_name = "Numeric Comparison w/ Tolerance"
    comparison_class = "compare-tolerance"
    persist_attributes = ["baseline_value", "tolerance"]

    def __init__(self, baseline_value, tolerance=0.5):
        self.baseline_value = baseline_value
        self.tolerance = abs(tolerance)

    def do_compare(self, cmp_value):
        return self.baseline_value - self.tolerance <= cmp_value <= self.baseline_value + self.tolerance
