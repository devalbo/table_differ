import re
from util import cell_comparison

@cell_comparison
class RegExCellComparison:
    comparison_name = "Regular Expression"
    comparison_class = "compare-regex"
    persist_attributes = ["baseline_value"]

    def __init__(self, baseline_value):
        self.baseline_value = baseline_value

    def __str__(self):
        return self.baseline_value

    def __unicode__(self):
        return self.baseline_value

    def do_compare(self, cmp_value):
        rx = re.compile("^%s$" % self.baseline_value)
        return rx.match(cmp_value) is not None

