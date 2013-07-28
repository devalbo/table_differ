import re
from collections import OrderedDict

_CELL_COMPARISONS = OrderedDict()


def cell_comparison(cls):
    _CELL_COMPARISONS[cls.comparison_name] = cls
    return cls

@cell_comparison
class LiteralCellComparison:
    comparison_name = "Literal"
    comparison_class = "compare-literal"

    def __init__(self, baseline_value):
        self._baseline_value = baseline_value

    def __str__(self):
        return self._baseline_value

    def __unicode__(self):
        return self._baseline_value

    def do_compare(self, cmp_value):
        return self._baseline_value.strip() == cmp_value.strip()


@cell_comparison
class RegExCellComparison:
    comparison_name = "Regular Expression"
    comparison_class = "compare-regex"

    def __init__(self, baseline_value):
        self._baseline_value = baseline_value

    def __str__(self):
        return self._baseline_value

    def __unicode__(self):
        return self._baseline_value

    def do_compare(self, cmp_value):
        rx = re.compile("^%s$" % self._baseline_value)
        return rx.match(cmp_value) is not None


@cell_comparison
class IgnoreDifferencesComparison:
    comparison_name = "Ignore"
    comparison_class = "compare-ignore"

    def __init__(self, baseline_value):
        self._baseline_value = baseline_value

    def __str__(self):
        return self._baseline_value

    def __unicode__(self):
        return self._baseline_value

    def do_compare(self, cmp_value):
        return True


@cell_comparison
class NumberToleranceCellComparison:
    comparison_name = "Numeric Comparison w/ Tolerance"
    comparison_class = "compare-tolerance"

    def __init__(self, baseline_value, tolerance=0.5):
        self._baseline_value = baseline_value
        self._tolerance = abs(tolerance)

    def do_compare(self, cmp_value):
        return self._baseline_value - self._tolerance <= cmp_value <= self._baseline_value + self._tolerance


def get_constructor_for_comparison_class(comparison_class):
    for v in _CELL_COMPARISONS.values():
        if v.comparison_class == comparison_class:
            return v
    return None

CHOICES = OrderedDict([(i, k) for i, k in enumerate(_CELL_COMPARISONS.keys())])
IDS_TO_CHOICE_NAMES_DICT = dict([(k, i) for i, k in enumerate(_CELL_COMPARISONS.keys())])


def get_comparison_class_for_type(cmp_type):
    return _CELL_COMPARISONS[CHOICES[cmp_type]]


COMPARISON_TYPE_TO_CSS_DICT = {
    0: "compare-literal",
    1: "compare-regex",
    2: "compare-ignore",
    }

def css_for_comparison_type(comparison_type):
    return COMPARISON_TYPE_TO_CSS_DICT[comparison_type]

