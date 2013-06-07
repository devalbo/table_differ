
import logging
import td_comparison

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def compare_tables(t1, t2, comparator):
    comparison = td_comparison.TdComparison(t1, t2)
    comparison.do_comparison(comparator)
    return comparison
