
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from table_differ import td_parsers
import unittest


class TestTdParsers(unittest.TestCase):

    def test_loading_xls_file(self):
        t = td_parsers.load_table_from_xls("test_data/test_sheet.xls",
                                           worksheet_name="MainSheet")

        self.assertEqual("Test", t.get_value(0, 0))
        self.assertEqual("The Corner", t.get_value(16, 6))
        self.assertEqual("495.0", t.get_value(10, 4))
        self.assertEqual(495.0, t.get_value(10, 4, False))
        self.assertEqual("1/13/2013", t.get_value(0, 1))


    def test_loading_handson_json_data(self):
        with open("test_data/test_sheet.handson.json", "r") as f:
            data = f.read().replace('\n', '')
        t = td_parsers.load_table_from_handson_json(data)

        self.assertEqual("Test", t.get_value(1, 1))
        self.assertEqual("abc", t.get_value(0, 3))
        self.assertEqual("1/13/2012", t.get_value(5, 7))
        self.assertEqual("495", t.get_value(2, 6))


if __name__ == "__main__":
    unittest.main()