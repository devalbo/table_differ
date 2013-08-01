from util import cell_comparison

@cell_comparison
class IgnoreDifferencesComparison:
    comparison_type_id = -1  # automatically assigned at startup
    comparison_type_name = "cell.compare-ignore"
    comparison_css_class = "compare-ignore"
    comparison_label = "Ignore"
    persist_attributes = ["baseline_value"]

    def __init__(self, baseline_value):
        self.baseline_value = baseline_value

    def __str__(self):
        return self.baseline_value

    def __unicode__(self):
        return self.baseline_value

    def do_compare(self, cmp_value):
        return True
