import re

COMPARE_LITERAL = "Literal"
COMPARE_RE_SKIP = "Regular Expression"

class TdComparison:

    def __init__(self, expected_table, actual_table):
        self._expected_table = expected_table
        self._actual_table = actual_table
        self._diff_cells = None
        self._same_cells = None
        self._expected_table_only_cells = None
        self._actual_table_only_cells = None
        self._neither_table_cell_coords = None
        self._comparison_notes = []
        self._comparator = None

    def do_comparison(self, comparator):
        if comparator == COMPARE_LITERAL:
            self._do_compare_literal()
        elif comparator == COMPARE_RE_SKIP:
            self._do_compare_re_skip()
        else:
            raise Exception("No such comparator: %s" % comparator)

        self._comparator = comparator

    @property
    def max_rows(self):
        return max(self._expected_table.row_count, self._actual_table.row_count)

    @property
    def max_cols(self):
        return max(self._expected_table.col_count, self._actual_table.col_count)

    @property
    def expected_table(self):
        return self._expected_table

    @property
    def actual_table(self):
        return self._actual_table

    @property
    def diff_cells(self):
        return self._diff_cells

    @property
    def same_cells(self):
        return self._same_cells

    @property
    def expected_table_only_cells(self):
        return self._expected_table_only_cells

    @property
    def actual_table_only_cells(self):
        return self._actual_table_only_cells

    @property
    def neither_table_cell_coords(self):
        return self._neither_table_cell_coords

    @property
    def comparison_notes(self):
        return self._comparison_notes

    @property
    def tables_equivalent(self):
        if self._comparator is None:
            raise Exception("No comparison performed yet")

        if len(self.diff_cells) > 0:
            return False
        if len(self.expected_table_only_cells) > 0:
            return False
        if len(self.actual_table_only_cells) > 0:
            return False

        if len(self.same_cells) == 0:
            if self.max_rows > 0 or self.max_cols > 0:
                return False

        return True

    def _do_compare_literal(self):
        def literal_compare_func(expected_value, actual_value):
            return expected_value == actual_value

        return self._do_compare(literal_compare_func)

    def _do_compare_re_skip(self):
        def re_compare_func(expected_value, actual_value):
            rx = re.compile("^%s$" % expected_value)
            return rx.match(actual_value) is not None

        return self._do_compare(re_compare_func)

    def _do_compare(self, compare_func):
        diffs = {}
        sames = {}
        expected_table_only_cells = {}
        actual_table_only_cells = {}
        neither_table_cell_coords = []

        for row_index in range(self.max_rows):
            for col_index in range(self.max_cols):

                expected_table_cell_found = False
                actual_table_cell_found = False

                try:
                    expected_table_cell_value = self._expected_table.get_value(row_index, col_index)
                    expected_table_cell_found = True
                except (KeyError, IndexError):
                    try:
                        actual_table_only_cells[(row_index, col_index)] = self._actual_table.get_value(row_index, col_index)
                    except (KeyError, IndexError):
                        pass

                try:
                    actual_table_cell_value = self._actual_table.get_value(row_index, col_index)
                    actual_table_cell_found = True
                except (KeyError, IndexError):
                    try:
                        expected_table_only_cells[(row_index, col_index)] = self._expected_table.get_value(row_index, col_index)
                    except (KeyError, IndexError):
                        pass

                if expected_table_cell_found and actual_table_cell_found:
                    if compare_func(expected_table_cell_value, actual_table_cell_value):
                        sames[(row_index, col_index)] = expected_table_cell_value
                    else:
                        diffs[(row_index, col_index)] = (expected_table_cell_value, actual_table_cell_value)

                elif not expected_table_cell_found and not actual_table_cell_found:
                    neither_table_cell_coords.append((row_index, col_index))

        self._same_cells = sames
        self._diff_cells = diffs
        self._expected_table_only_cells = expected_table_only_cells
        self._actual_table_only_cells = actual_table_only_cells
        self._neither_table_cell_coords = neither_table_cell_coords

