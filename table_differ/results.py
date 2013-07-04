
from flask import Blueprint, render_template, abort, request, url_for, Markup
import td_config, td_persist

blueprint = Blueprint('results', __name__,
                      template_folder='templates')


@blueprint.route('/<comparison_id>', methods=['GET'])
def show_results(comparison_id):
    options = td_config.RenderTableOptions()

    report_notes = []

    comparison = td_persist.retrieve_new_comparison(comparison_id)
    expected_row_count = comparison.expected_table.row_count
    actual_row_count = comparison.actual_table.row_count
    if expected_row_count != actual_row_count:
        report_note = "Error - different numbers of rows (Expected: %s / Actual: %s)" % (expected_row_count,
                                                                                         actual_row_count)
        report_notes.append(report_note)

    expected_col_count = comparison.expected_table.col_count
    actual_col_count = comparison.actual_table.col_count
    if expected_col_count != actual_col_count:
        report_note = "Error - different numbers of columns (Expected: %s / Actual: %s)" % (expected_col_count,
                                                                                            actual_col_count)
        report_notes.append(report_note)

    if not comparison.tables_equivalent:
        report_note = "Error - %s different cells; %s cells are the same" % (len(comparison.diff_cells),
                                                                             len(comparison.same_cells))
        report_notes.append(report_note)

    cd = comparison.diff_cells.keys()[:]
    cd.sort()
    for cell in cd:
        report_notes.append("[%s,%s] Expected: %s Actual: %s" %
                            (cell[0], cell[1],
                             comparison.expected_table.get_value(cell[0], cell[1]),
                             comparison.actual_table.get_value(cell[0], cell[1])))

    if len(report_notes) == 0:
        report_notes.append("No differences between expected and actual tables")

    table_rows = []
    for row_index in range(comparison.max_rows):
        table_row = []
        for col_index in range(comparison.max_cols):
            if (row_index, col_index) in comparison.same_cells:
                item = ("%s" % comparison.same_cells[(row_index, col_index)], "ok")
            elif (row_index, col_index) in comparison.diff_cells:
                item = (Markup("Expected: %s<br>Actual: %s" %
                               comparison.diff_cells[(row_index, col_index)]),
                        "mismatch")
            elif (row_index, col_index) in comparison.expected_table_only_cells:
                item = (Markup("Expected: %s<br>Actual: --missing--" %
                               comparison.expected_table_only_cells[(row_index, col_index)]),
                        "missing_expected")
            elif (row_index, col_index) in comparison.actual_table_only_cells:
                item = (Markup("Expected: --missing--<br>Actual: %s" %
                               comparison.actual_table_only_cells[(row_index, col_index)]),
                        "missing_actual")
            elif (row_index, col_index) in comparison.neither_table_cell_coords:
                item = ("", "padding")
            else:
                raise Exception("Untreated cell: %s" % ((row_index, col_index)))

            table_row.append(item)

        table_rows.append(table_row)

    return render_template('comparison_results.html',
                           table_rows=table_rows,
                           report_notes=report_notes,
                           options=options,
                           header_tab_classes={},
                           comparison_id=comparison_id)