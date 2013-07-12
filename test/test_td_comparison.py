__author__ = 'ajboehmler'

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from table_differ import td_table, td_comparison
import unittest


class TestTdComparison(unittest.TestCase):

    def test_comparison_performed_check(self):
        expected_table = td_table.TdTable()
        actual_table = td_table.TdTable()

        with self.assertRaises(Exception) as cm:
            comparison = td_comparison.TdComparison(expected_table, actual_table)
            equivalent = comparison.tables_equivalent

        the_exception = cm.exception
        self.assertEqual("No comparison performed yet", the_exception.message)

    def test_comparing_same_literal(self):
        expected_table = td_table.TdTable()
        actual_table = td_table.TdTable()

        for r in [["a1", "a2", "a3"],
                  ["b1", "b2", "b3"],
                  ["c1", "c2", "c3"]]:
            expected_table.add_row(r)
            actual_table.add_row(r)

        comparison = td_comparison.TdComparison(expected_table, actual_table)
        comparison.do_comparison(td_comparison.COMPARE_LITERAL)

        self.assertTrue(comparison.tables_equivalent)
        self.assertEqual(0, len(comparison.diff_cells))
        self.assertEqual(9, len(comparison.same_cells))
        self.assertEqual(0, len(comparison.expected_table_only_cells))
        self.assertEqual(0, len(comparison.actual_table_only_cells))

    def test_comparing_different_literal_same_size(self):
        expected_table = td_table.TdTable()
        actual_table = td_table.TdTable()

        for r in [["a1", "a2", "a3"],
                  ["b1", "b2", "b3"],
                  ["c1", "c2", "c3"]]:
            expected_table.add_row(r)

        for r in [["1a", "a2", "a3"],
                  ["b1", "2b", "b3"],
                  ["c1", "c2", "3c"]]:
            actual_table.add_row(r)

        comparison = td_comparison.TdComparison(expected_table, actual_table)
        comparison.do_comparison(td_comparison.COMPARE_LITERAL)

        self.assertFalse(comparison.tables_equivalent)
        self.assertEqual(3, len(comparison.diff_cells))
        self.assertEqual(6, len(comparison.same_cells))
        self.assertEqual(0, len(comparison.expected_table_only_cells))
        self.assertEqual(0, len(comparison.actual_table_only_cells))
        self.assertEqual(0, len(comparison.neither_table_cell_coords))

    def test_comparing_different_literal_t1_bigger(self):
        expected_table = td_table.TdTable()
        actual_table = td_table.TdTable()

        for r in [["a1", "a2", "a3", "a4"],
                  ["b1", "b2", "b3", "b4"],
                  ["c1", "c2", "c3", "c4"],
                  ["d1", "d2", "d3", "d4"]]:
            expected_table.add_row(r)

        for r in [["a1", "a2", "a3"],
                  ["b1", "b2", "b3"],
                  ["c1", "c2", "c3"]]:
            actual_table.add_row(r)

        comparison = td_comparison.TdComparison(expected_table, actual_table)
        comparison.do_comparison(td_comparison.COMPARE_LITERAL)

        self.assertFalse(comparison.tables_equivalent)
        self.assertEqual(0, len(comparison.diff_cells))
        self.assertEqual(9, len(comparison.same_cells))
        self.assertEqual(7, len(comparison.expected_table_only_cells))
        self.assertEqual(0, len(comparison.actual_table_only_cells))
        self.assertEqual(0, len(comparison.neither_table_cell_coords))

    def test_comparing_different_literal_t2_bigger(self):
        expected_table = td_table.TdTable()
        actual_table = td_table.TdTable()

        for r in [["a1", "a2", "a3"],
                  ["b1", "b2", "b3"],
                  ["c1", "c2", "c3"]]:
            expected_table.add_row(r)

        for r in [["a1", "a2", "a3", "a4"],
                  ["b1", "b2", "b3", "b4"],
                  ["c1", "c2", "c3", "c4"],
                  ["d1", "d2", "d3", "d4"]]:
            actual_table.add_row(r)

        comparison = td_comparison.TdComparison(expected_table, actual_table)
        comparison.do_comparison(td_comparison.COMPARE_LITERAL)

        self.assertFalse(comparison.tables_equivalent)
        self.assertEqual(0, len(comparison.diff_cells))
        self.assertEqual(9, len(comparison.same_cells))
        self.assertEqual(0, len(comparison.expected_table_only_cells))
        self.assertEqual(7, len(comparison.actual_table_only_cells))
        self.assertEqual(0, len(comparison.neither_table_cell_coords))

    def test_comparing_different_literal_inverted_tables(self):
        expected_table = td_table.TdTable()
        actual_table = td_table.TdTable()

        for r in [["a1", "a2", "a3"],
                  ["b1", "b2", "b3"],
                  ["c1", "c2", "c3"],
                  ["d1", "d2", "d3"]]:
            expected_table.add_row(r)

        for r in [["a1", "a2", "a3", "a4"],
                  ["b1", "b2", "b3", "b4"],
                  ["c1", "c2", "c3", "c4"]]:
            actual_table.add_row(r)

        comparison = td_comparison.TdComparison(expected_table, actual_table)
        comparison.do_comparison(td_comparison.COMPARE_LITERAL)

        self.assertFalse(comparison.tables_equivalent)
        self.assertEqual(0, len(comparison.diff_cells))
        self.assertEqual(9, len(comparison.same_cells))
        self.assertEqual(3, len(comparison.expected_table_only_cells))
        self.assertEqual(3, len(comparison.actual_table_only_cells))
        self.assertEqual(1, len(comparison.neither_table_cell_coords))

    def test_comparing_different_re_tables(self):
        expected_table = td_table.TdTable()
        actual_table = td_table.TdTable()

        for r in [["", "a2", "a3"],
                  ["b1", "", "b3"],
                  ["c1", "c2", "c3"]]:
            expected_table.add_row(r)

        for r in [["a1", "a2", "a3"],
                  ["b1", "b2", "b3"],
                  ["c1", "c2", "c3"]]:
            actual_table.add_row(r)

        comparison = td_comparison.TdComparison(expected_table, actual_table)
        comparison.do_comparison(td_comparison.COMPARE_RE_SKIP)

        self.assertFalse(comparison.tables_equivalent)
        print comparison.diff_cells
        self.assertEqual(2, len(comparison.diff_cells))
        self.assertEqual(7, len(comparison.same_cells))
        self.assertEqual(0, len(comparison.expected_table_only_cells))
        self.assertEqual(0, len(comparison.actual_table_only_cells))


    def test_comparing_different_re_tables(self):
        expected_table = td_table.TdTable()
        actual_table = td_table.TdTable()

        for r in [["", "a2", "a3"],
                  ["b1", "", "b3"],
                  ["c1", "c2", "c3"]]:
            expected_table.add_row(r)

        for r in [["a1", "a2", "a3"],
                  ["b1", "b2", "b3"],
                  ["c1", "c2", "c3"]]:
            actual_table.add_row(r)

        comparison = td_comparison.TdComparison(expected_table, actual_table)
        comparison.do_comparison(td_comparison.COMPARE_RE_SKIP)

        self.assertFalse(comparison.tables_equivalent)
        print comparison.diff_cells
        self.assertEqual(2, len(comparison.diff_cells))
        self.assertEqual(7, len(comparison.same_cells))
        self.assertEqual(0, len(comparison.expected_table_only_cells))
        self.assertEqual(0, len(comparison.actual_table_only_cells))


    def test_updating_expected_to_actual(self):
        self.assertFalse(True)


if __name__ == "__main__":
    unittest.main()