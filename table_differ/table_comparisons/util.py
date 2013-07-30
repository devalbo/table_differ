from collections import OrderedDict
import json

TABLE_COMPARISONS = OrderedDict()
CHOICES = OrderedDict()


def table_comparison(cls):
    TABLE_COMPARISONS[cls.comparison_name] = cls
    CHOICES[len(TABLE_COMPARISONS) - 1] = cls.comparison_name
    return cls


def get_comparison_class_for_type(cmp_type):
    return TABLE_COMPARISONS[CHOICES[cmp_type]]


def get_constructor_for_comparison_name(comparison_name):
    for v in TABLE_COMPARISONS.values():
        if v.comparison_name == comparison_name:
            return v
    return None


def get_json_dict_for_comparison(cmp):
    d = {}
    d["comparison_name"] = cmp.comparison_name
    attributes = {}
    for attribute in cmp.persist_attributes:
        attributes[attribute] = getattr(cmp, attribute)
    d["attributes"] = attributes
    return d


def create_comparison_from_json(cmp_json):
    json_data = json.loads(cmp_json)
    comparison_name = json_data["comparison_name"]
    for v in TABLE_COMPARISONS.values():
        if v.comparison_name == comparison_name:
            constructor = get_constructor_for_comparison_name(comparison_name)
            comparison = constructor()
            attributes = json_data["attributes"]
            for attr in attributes:
                setattr(comparison, attr, attributes[attr])
            return comparison
