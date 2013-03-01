
from datetime import datetime
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def compare_tabular_inputs(in_1, in_2, col_item_comparisons={}):
    LOG_FILENAME = "%s_%s_%s_%s_%s_%s.log" % datetime.timetuple(datetime.now())[0:6]
    file_handler = logging.FileHandler(LOG_FILENAME)
    logger.addHandler(file_handler)

    lines_1 = in_1.split("\n")
    lines_2 = in_2.split("\n")
    headers_1 = lines_1[0].split("\t")
    headers_2 = lines_2[0].split("\t")

    if len(lines_1) != len(lines_2):
        logging.warning("Number of lines of data not equal: %s vs. %s<br>" %
                        (len(lines_1), len(lines_2)))

    for h1, h2 in zip(headers_1, headers_2):
        if h1 != h2:
            logging.warning("Headers not equal (%s/%s)<br>" % (h1, h2))

    header_index_map = {}
    value_lists = {}
    index = 0
    for h in headers_1:
        header_index_map[index] = h
        value_lists[h] = []
        index += 1

    line_no = 2
    for i1, i2 in zip(lines_1[1:], lines_2[1:]):
        line_1 = i1.split("\t")
        line_2 = i2.split("\t")
        if len(line_1) != len(line_2):
            logging.warning("Different number of elements at line %s<br>" % line_no)

        index = 0
        for item_1, item_2 in zip(line_1, line_2):
            if not check_for_equal(item_1, item_2):
                logging.warning("Mismatch at line %s for item %s (%s/%s)<br>" % 
                    (line_no, header_index_map[index], item_1, item_2))
            index += 1

        line_no += 1
            
    logger.removeHandler(file_handler)
    file_handler.flush()

    f = open(LOG_FILENAME)
    contents = f.read()
    f.close()
    return contents

def compare_tabular_inputs_with_tolerance(in_1, in_2, col_item_comparisons={}):
    LOG_FILENAME = "%s_%s_%s_%s_%s_%s.log" % datetime.timetuple(datetime.now())[0:6]
    file_handler = logging.FileHandler(LOG_FILENAME)
    logger.addHandler(file_handler)

    lines_1 = in_1.split("\n")
    lines_2 = in_2.split("\n")
    headers_1 = lines_1[0].split("\t")
    headers_2 = lines_2[0].split("\t")

    if len(lines_1) != len(lines_2):
        logging.warning("Number of lines of data not equal: %s vs. %s" %
                        (len(lines_1), len(lines_2)))

    for h1, h2 in zip(headers_1, headers_2):
        if h1 != h2:
            logging.warning("Headers not equal (%s/%s)" % (h1, h2))

    header_index_map = {}
    value_lists = {}
    index = 0
    for h in headers_1:
        header_index_map[index] = h
        value_lists[h] = []
        index += 1

    line_no = 2
    for i1, i2 in zip(lines_1[1:], lines_2[1:]):
        line_1 = i1.split("\t")
        line_2 = i2.split("\t")
        if len(line_1) != len(line_2):
            logging.warning("Different number of elements at line %s" % line_no)

        index = 0
        for item_1, item_2 in zip(line_1, line_2):
            if index == 0:
                if not check_for_equal(item_1, item_2):
                    logging.warning("Mismatch at line %s for item %s (%s/%s)" % 
                        (line_no, header_index_map[index], item_1, item_2))
            else:
                if not check_for_float_equivalence(item_1, item_2):
                    logging.warning("Mismatch at line %s for item %s (%s/%s)" % 
                        (line_no, header_index_map[index], item_1, item_2))
            index += 1

        line_no += 1
            
    logger.removeHandler(file_handler)
    file_handler.flush()

    f = open(LOG_FILENAME)
    contents = f.read()
    f.close()
    return contents


def check_for_equal(item_1, item_2):
    return item_1 == item_2

float_equivalence_tolerance = 1/float(pow(10, 10))
#print "Tolerance: %s" % float_equivalence_tolerance
def check_for_float_equivalence(item_1, item_2):
    f_item1 = float(item_1)
    f_item2 = float(item_2)
    return abs(f_item1 - f_item2) < float_equivalence_tolerance

def compare_tables(t1, t2, comparator):
    diffs = {}
    sames = {}
    for row_index, (t1_row, t2_row) in enumerate(zip(t1, t2)):
        for col_index, (t1_cell, t2_cell) in enumerate(zip(t1_row, t2_row)):
##            print "C-%s:%s" % (row_index, col_index), t1_cell
            if t1_cell != t2_cell:
                diffs[(row_index, col_index)] = (t1_cell, t2_cell)
            else:
                sames[(row_index, col_index)] = t1_cell
                
    return diffs, sames

if __name__ == "__main__":
    t1 = [[str(i) for i in range(10)] for i in range(10)]
    t2 = [[str(i) for i in range(10, 0, -1)] for i in range(10, 0, -1)]
##    t2 = t1
    diffs = compare_tables(t1, t2, None)
    print diffs
