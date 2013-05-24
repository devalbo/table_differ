__author__ = 'ajboehmler'

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from table_differ import td_table
import unittest


class TestTdTable(unittest.TestCase):

    def test_properties(self):
        table = td_table.TdTable()
        r1 = ["a1", "a2", "a3"]
        r2 = ["b1", "b2", "b3"]
        r3 = ["c1", "c2", "c3"]
        table.add_row(r1)
        table.add_row(r2)
        table.add_row(r3)

        self.assertEqual([r1, r2, r3],
                         table.rows)

        self.assertEqual(3, table.row_count)
        self.assertEqual(3, table.col_count)

    def test_get_value(self):
        table = td_table.TdTable()
        r1 = ["a1", "a2", "a3"]
        r2 = ["b1", "b2", "b3"]
        r3 = ["c1", "c2", "c3"]
        table.add_row(r1)
        table.add_row(r2)
        table.add_row(r3)

        self.assertEqual("a1", table.get_value(0, 0))
        self.assertEqual("a2", table.get_value(0, 1))
        self.assertEqual("b1", table.get_value(1, 0))
        self.assertEqual("c2", table.get_value(2, 1))
        self.assertEqual("c3", table.get_value(2, 2))



if __name__ == "__main__":
    unittest.main()