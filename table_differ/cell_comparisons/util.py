
CHOICE_LABELS = []
CELL_COMPARISONS = {}
IDS_TO_CMP_CLASS_DICT = {}
IDS_TO_CMP_LABEL_DICT = {}
IDS_TO_CMP_CSS_DICT = {}


def cell_comparison(cls):
    cmp_index = len(CELL_COMPARISONS)
    cls.comparison_type_id = cmp_index
    CELL_COMPARISONS[cls.comparison_type_id] = cls
    CHOICE_LABELS.append((cmp_index, cls.comparison_label))
    IDS_TO_CMP_CLASS_DICT[cmp_index] = cls
    IDS_TO_CMP_LABEL_DICT[cmp_index] = cls.comparison_label
    IDS_TO_CMP_CSS_DICT[cmp_index] = cls.comparison_css_class
    return cls


def get_comparison_class_for_type(cmp_type):
    return IDS_TO_CMP_CLASS_DICT[cmp_type]


def get_constructor_for_comparison_type(comparison_type_name):
    for v in CELL_COMPARISONS.values():
        if v.comparison_type_name == comparison_type_name:
            return v
    return None


def css_for_comparison_type(comparison_type):
    return IDS_TO_CMP_CSS_DICT[comparison_type]


def name_for_comparison_type(comparison_type):
    return CHOICE_LABELS[comparison_type][1]


def get_json_dict_for_comparison(cmp):
    attributes = {}
    for attribute in cmp.persist_attributes:
        attributes[attribute] = getattr(cmp, attribute)

    d = {
        "cell_cmp_type": cmp.comparison_type_name,
        "cell_cmp_attributes": attributes,
        }

    return d


def create_comparison_from_json_dict(cmp_dict):
    comparison_type = cmp_dict["cell_cmp_type"]
    for v in CELL_COMPARISONS.values():
        if v.comparison_type_name == comparison_type:
            constructor = get_constructor_for_comparison_type(comparison_type)
            comparison = constructor(None)
            attributes = cmp_dict["cell_cmp_attributes"]
            for attr in attributes:
                setattr(comparison, attr, attributes[attr])
            return comparison
