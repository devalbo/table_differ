from util import cell_comparison

@cell_comparison
class LiteralCellComparison:
    comparison_name = "Literal"
    comparison_class = "compare-literal"
    persist_attributes = ["baseline_value"]

    def __init__(self, baseline_value):
        self.baseline_value = baseline_value

    def __str__(self):
        return self.baseline_value

    def __unicode__(self):
        return self.baseline_value

    def do_compare(self, cmp_value):
        return self.baseline_value.strip() == cmp_value.strip()
