
from collections import OrderedDict

CELL_COMPARISONS = OrderedDict()
CHOICES = OrderedDict()
IDS_TO_CHOICE_NAMES_DICT = {}
COMPARISON_TYPE_TO_CSS_DICT = {}


def cell_comparison(cls):
    CELL_COMPARISONS[cls.comparison_name] = cls
    CHOICES[len(CELL_COMPARISONS) - 1] = cls.comparison_name
    IDS_TO_CHOICE_NAMES_DICT[cls.comparison_name] = len(CELL_COMPARISONS) - 1
    COMPARISON_TYPE_TO_CSS_DICT[len(CELL_COMPARISONS) - 1] = cls.comparison_class
    return cls


def get_comparison_class_for_type(cmp_type):
    return CELL_COMPARISONS[CHOICES[cmp_type]]


def get_constructor_for_comparison_class(comparison_class):
    for v in CELL_COMPARISONS.values():
        if v.comparison_class == comparison_class:
            return v
    return None


def css_for_comparison_type(comparison_type):
    return COMPARISON_TYPE_TO_CSS_DICT[comparison_type]


def name_for_comparison_type(comparison_type):
    return CHOICES[comparison_type]


def get_json_dict_for_comparison(cmp):
    d = {}
    d["comparison_class"] = cmp.comparison_class
    attributes = {}
    for attribute in cmp.persist_attributes:
        attributes[attribute] = getattr(cmp, attribute)
    d["attributes"] = attributes
    return d


def create_comparison_from_json_dict(cmp_dict):
    comparison_class = cmp_dict["comparison_class"]
    for v in CELL_COMPARISONS.values():
        if v.comparison_class == comparison_class:
            constructor = get_constructor_for_comparison_class(comparison_class)
            comparison = constructor(None)
            attributes = cmp_dict["attributes"]
            for attr in attributes:
                setattr(comparison, attr, attributes[attr])
            return comparison
