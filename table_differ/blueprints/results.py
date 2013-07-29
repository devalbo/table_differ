
import pickle, StringIO
from flask import Blueprint, render_template, request, Markup, send_file, jsonify
import td_config, td_comparison
import models

blueprint = Blueprint('results', __name__,
                      template_folder='templates')

@blueprint.route('/')
def show_results():
    results = models.ComparisonResult.select()
    return render_template('list_results.html',
                           header_tab_classes={'compare-results': 'active'},
                           results=results)

@blueprint.route('/<comparison_id>')
def show_result(comparison_id):
    options = td_config.RenderTableOptions()

    report_notes = []

    cr = models.ComparisonResult.get(models.ComparisonResult.id == comparison_id)
    comparison = pickle.loads(cr.pickled_comparison_report)
    baseline_grid_row_count = comparison.baseline_grid.row_count
    actual_row_count = comparison.actual_table.row_count
    if baseline_grid_row_count != actual_row_count:
        report_note = "Error - different numbers of rows (Expected: %s / Actual: %s)" % (baseline_grid_row_count,
                                                                                         actual_row_count)
        report_notes.append(report_note)

    baseline_grid_col_count = comparison.baseline_grid.col_count
    actual_col_count = comparison.actual_table.col_count
    if baseline_grid_col_count != actual_col_count:
        report_note = "Error - different numbers of columns (Expected: %s / Actual: %s)" % (baseline_grid_col_count,
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
                            (cell[0],
                             cell[1],
                             comparison.baseline_grid.get_expected_value(cell[0], cell[1]),
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

    baseline_id = cr.baseline.id

    return render_template('comparison_results.html',
                           table_rows=table_rows,
                           report_notes=report_notes,
                           options=options,
                           header_tab_classes={'compare-results': 'active'},
                           comparison_id=comparison_id,
                           baseline_id=baseline_id)

@blueprint.route('/<comparison_id>/results-grid-data')
def view_results_grid_data(comparison_id):
    cr = models.ComparisonResult.get(models.ComparisonResult.id == comparison_id)
    comparison = pickle.loads(cr.pickled_comparison_report)

    items = []
    item_styles = []
    for row_index in range(comparison.max_rows):
        items_row = []
        item_styles_row = []
        for col_index in range(comparison.max_cols):
            if (row_index, col_index) in comparison.same_cells:
                items_row.append(comparison.same_cells[(row_index, col_index)])
                item_styles_row.append("ok")
            elif (row_index, col_index) in comparison.diff_cells:
                items_row.append(Markup("Expected: %s\nActual: %s" %
                               comparison.diff_cells[(row_index, col_index)]))
                item_styles_row.append("mismatch")
            elif (row_index, col_index) in comparison.expected_table_only_cells:
                items_row.append(Markup("Expected: %s\nActual: --missing--" %
                               comparison.expected_table_only_cells[(row_index, col_index)]))
                item_styles_row.append("missing_expected")
            elif (row_index, col_index) in comparison.actual_table_only_cells:
                items_row.append(Markup("Expected: --missing--\nActual: %s" %
                               comparison.actual_table_only_cells[(row_index, col_index)]))
                item_styles_row.append("missing_actual")
            elif (row_index, col_index) in comparison.neither_table_cell_coords:
                items_row.append("")
                item_styles_row.append("padding")
            else:
                raise Exception("Untreated cell: %s" % ((row_index, col_index)))

        items.append(items_row)
        item_styles.append(item_styles_row)

    response = {"result": "ok",
                "data": {"cells": items,
                         "cell_statuses": item_styles,
                        }
                }
    return jsonify(response)

@blueprint.route('/<comparison_id>/results-grid-data', methods=['POST'])
def update_results_grid_data(comparison_id):
    cr = models.ComparisonResult.get(models.ComparisonResult.id == comparison_id)
    update_action = request.json['update_type']
    update_args = request.json['update_args']

    updated_items = td_comparison.do_results_update(cr, update_action, update_args)
    if updated_items:
        for i in updated_items:
            i.save()

    return jsonify({})


@blueprint.route('/thumbnails/<comparison_id>')
def thumbnails(comparison_id):
    img = models.ComparisonResult.get(models.ComparisonResult.id == comparison_id).comparison_image

    strIO = StringIO.StringIO()
    strIO.write(img)
    strIO.seek(0)
    return send_file(strIO,
                     attachment_filename="comparison-overview-%s.png" % comparison_id,
                     as_attachment=True)


