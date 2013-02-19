
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

_file_handler = logging.FileHandler('verify_lists.log')
logger.addHandler(_file_handler)


def verify_lists(list1, list2, qualifier="contains", report=False):
    list1_items = list1.split(";")
    list2_items = list2.split(";")
    
    if qualifier == "contains":
        return _verify_lists_contains(list1_items, list2_items)
    
    elif qualifier == "only contains":
        return _verify_lists_only_contains(list1_items, list2_items)
    
    elif qualifier == "contains in order":
        return _verify_lists_contains_in_order(list1_items, list2_items)
    
    elif qualifier == "does not contain":
        return _verify_lists_does_not_contain(list1_items, list2_items)
    
    else:
        raise Exception('invalid qualifier for verify_lists', qualifier)


def _verify_lists_contains_in_order(list1_items, list2_items):
    if len(list1_items) < len(list2_items):
        logging.info("Fail (contains in order): Only %s items in expected list '%s' to compare to %s items in actual list '%s'" %
                     (len(list1_items), ";".join(list1_items), len(list2_items), ";".join(list2_items)))
        return False
        
    verify = True
    for list1_item, list2_item in zip(list1_items, list2_items):
        if list1_item != list2_item:
            verify = False
            break

    if verify:
        logging.info("Pass (contains in order): Verified expected list '%s' contains in order actual list '%s'" %
                     (";".join(list1_items), ";".join(list2_items)))
        return True
    else:
        logging.info("Fail (contains in order): Order of items in expected list '%s' does not match order of items in actual list '%s'" %
                     (";".join(list1_items), ";".join(list2_items)))
        return False


def _verify_lists_does_not_contain(list1_items, list2_items):
    list1_set = set(list1_items)
    list2_set = set(list2_items)
    if len(list1_set.intersection(list2_set)) == 0:
        logging.info("Pass (does not contain): Verified expected list '%s' does not contain actual list '%s'" %
                     (";".join(list1_items), ";".join(list2_items)))
        return True
    else:
        intersection = list1_set.intersection(list2_set)
        logging.info("Fail (does not contain): Expected list '%s' contains '%s' and should NOT [actual list is '%s']" %
                     (";".join(list1_items), ";".join(intersection), ";".join(list2_items)))
        return False


def _verify_lists_only_contains(list1_items, list2_items):
    list1_set = set(list1_items)
    list2_set = set(list2_items)
    if list1_set == list2_set:
        logging.info("Pass (only contains): Verified list %s contains %s" %
                     (";".join(list1_items), ";".join(list2_items)))
        return True
    else:
        missing_items = list1_set.difference(list2_set)
        extra_items = list2_set.difference(list1_set)
        logging.info("Fail (only contains): Expected list '%s' is MISSING '%s' and actual list contains extras '%s' [actual list is '%s']" %
                     (";".join(list1_items), ";".join(missing_items),
                      ";".join(extra_items), ";".join(list2_items)))
        return False


def _verify_lists_contains(list1_items, list2_items):
    list1_set = set(list1_items)
    list2_set = set(list2_items)
    if list2_set.issubset(list1_set):
        logging.info("Pass (contains): Verified expected list '%s' contains '%s'" %
                     (";".join(list1_items), ";".join(list2_items)))
        return True
    else:
        missing_items = list2_set.difference(list1_set)
        logging.info("Fail (contains): Expected list '%s' does NOT contain '%s' [actual list is '%s']" %
                     (";".join(list1_items), ";".join(missing_items), ";".join(list2_items)))
        return False


# special logging capabilities used by test_server.py
def init_logging(log_file_name):
    stop_logging()
    _file_handler = logging.FileHandler(log_file_name)
    logger.addHandler(_file_handler)


def stop_logging():
    logger.removeHandler(_file_handler)
    _file_handler.flush()
