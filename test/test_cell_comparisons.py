__author__ = 'ajboehmler'

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from table_differ import cell_comparisons
import unittest


class TestTdBaseline(unittest.TestCase):

    def test_LiteralCellComparison_same(self):
        c = cell_comparisons.LiteralCellComparison("a")
        self.assertTrue(c.do_compare("a"))

    def test_LiteralCellComparison_different(self):
        c = cell_comparisons.LiteralCellComparison("a")
        self.assertFalse(c.do_compare("b"))

    def test_RegExCellComparison_same(self):
        c = cell_comparisons.RegExCellComparison("\d")
        self.assertTrue(c.do_compare("3"))
        self.assertTrue(c.do_compare("0"))

        c = cell_comparisons.RegExCellComparison("1")
        self.assertTrue(c.do_compare("1"))

    def test_RegExCellComparison_different(self):
        c = cell_comparisons.RegExCellComparison("\d")
        self.assertFalse(c.do_compare("a"))

        c = cell_comparisons.RegExCellComparison("9")
        self.assertFalse(c.do_compare("8"))

    def test_NumberToleranceCellComparison_same(self):
        c = cell_comparisons.NumberToleranceCellComparison(3, .5)
        self.assertTrue(c.do_compare(2.5))
        self.assertTrue(c.do_compare(2.7))
        self.assertTrue(c.do_compare(3))
        self.assertTrue(c.do_compare(3.2))
        self.assertTrue(c.do_compare(3.5))

        c = cell_comparisons.NumberToleranceCellComparison(-3, .5)
        self.assertTrue(c.do_compare(-2.5))
        self.assertTrue(c.do_compare(-2.7))
        self.assertTrue(c.do_compare(-3))
        self.assertTrue(c.do_compare(-3.2))
        self.assertTrue(c.do_compare(-3.5))

    def test_NumberToleranceCellComparison_different(self):
        c = cell_comparisons.NumberToleranceCellComparison(3, .5)
        self.assertFalse(c.do_compare(2.4))
        self.assertFalse(c.do_compare(0))
        self.assertFalse(c.do_compare(3.6))

        c = cell_comparisons.NumberToleranceCellComparison(-3, .5)
        self.assertFalse(c.do_compare(-3.6))
        self.assertFalse(c.do_compare(-2.45))
        self.assertFalse(c.do_compare(0))


if __name__ == "__main__":
    unittest.main()