import json

CHOICE_LABELS = []
TABLE_COMPARISONS = {}
IDS_TO_CMP_CLASS_DICT = {}
IDS_TO_CMP_LABEL_DICT = {}
IDS_TO_CMP_TYPE_DICT = {}


def table_comparison(cls):
    cmp_index = len(TABLE_COMPARISONS)
    cls.comparison_type_id = cmp_index
    TABLE_COMPARISONS[cls.comparison_type_id] = cls
    CHOICE_LABELS.append((cmp_index, cls.comparison_label))
    IDS_TO_CMP_CLASS_DICT[cmp_index] = cls
    IDS_TO_CMP_LABEL_DICT[cmp_index] = cls.comparison_label
    IDS_TO_CMP_TYPE_DICT[cmp_index] = cls.comparison_type_name
    return cls


def get_comparison_class_for_type(cmp_type):
    return TABLE_COMPARISONS[CHOICE_LABELS[cmp_type]]


def get_constructor_for_comparison_type(comparison_type_name):
    for v in TABLE_COMPARISONS.values():
        if v.comparison_type_name == comparison_type_name:
            return v
    return None


def get_json_for_comparison(cmp):
    attributes = {}
    for attribute in cmp.persist_attributes:
        attributes[attribute] = getattr(cmp, attribute)

    d = {
        "table_cmp_type": cmp.comparison_type_name,
        "table_cmp_attributes": attributes,
        }
    return json.dumps(d)


def create_comparison_from_json(cmp_json):
    json_data = json.loads(cmp_json)
    comparison_type = json_data["table_cmp_type"]
    for v in TABLE_COMPARISONS.values():
        if v.comparison_type_name == comparison_type:
            constructor = get_constructor_for_comparison_type(comparison_type)
            comparison = constructor()
            attributes = json_data["table_cmp_attributes"]
            for attr in attributes:
                setattr(comparison, attr, attributes[attr])
            return comparison
