import os
import datetime

from flask import render_template
from flask import jsonify
from flask import request
from flask import url_for
from flask import redirect
from flask import Markup
from flask import send_from_directory

from werkzeug import secure_filename

import models
import td_config
import td_parsers
import td_persist
import td_comparison
import td_thumbnail

from admin import admin
from api import api
from app import app

import compare
import baseline
import results

app.register_blueprint(compare.blueprint, url_prefix='/compare')
app.register_blueprint(baseline.blueprint, url_prefix='/baseline')
app.register_blueprint(results.blueprint, url_prefix='/results')


ALLOWED_EXTENSIONS = set(['xls', 'xlsx', 'csv'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# @app.route('/')
# @app.route('/copy-paste-compare', methods=['GET', 'POST'])
# def copy_paste_compare():
#     if request.method == 'GET':
#         return render_template('tables_input.html',
#                                header_tab_classes={'copy-paste-compare': 'active'})
#
#     table1 = td_parsers.load_table_from_handson_json(request.json['dataTable1'])
#     table2 = td_parsers.load_table_from_handson_json(request.json['dataTable2'])
#
#     comparison = td_comparison.compare_tables(table1, table2, td_comparison.COMPARE_LITERAL)
#     comparison_id = td_persist.store_new_comparison(comparison)
#     td_thumbnail.create_comparison_image(comparison, comparison_id)
#
#     redirect_url = url_for('show_results', comparison_id=comparison_id)
#     return jsonify(redirect_url=redirect_url)

# @app.route('/xls-worksheet-compare', methods=['GET', 'POST'])
# def xls_worksheet_compare():
#     if request.method == 'GET':
#         return render_template('xls_worksheet_compare.html',
#                                header_tab_classes={'xls-worksheet-compare': 'active'})
#
#     worksheet_results_file = request.files['worksheet_file']
#     if worksheet_results_file and allowed_file(worksheet_results_file.filename):
#         filename = secure_filename(worksheet_results_file.filename)
#         file_location = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         worksheet_results_file.save(file_location)
#
#         expected_worksheet_name = "Reference"
#         actual_worksheet_name = "Actual"
#
#         expected_results_table = td_parsers.load_table_from_xls(file_location, expected_worksheet_name)
#         actual_results_table = td_parsers.load_table_from_xls(file_location, actual_worksheet_name)
#
#         comparison = td_comparison.compare_tables(expected_results_table, actual_results_table, td_comparison.COMPARE_RE_SKIP)
#         comparison_id = td_persist.store_new_comparison(comparison)
#         td_thumbnail.create_comparison_image(comparison, comparison_id)
#
#         redirect_url = url_for('show_results', comparison_id=comparison_id)
#         return redirect(redirect_url)
#
#     return redirect(url_for('xls_worksheet_compare'))

# @app.route('/results/<comparison_id>', methods=['GET'])
# def show_results(comparison_id):
#     options = td_config.RenderTableOptions()
#
#     report_notes = []
#
#     comparison = td_persist.retrieve_new_comparison(comparison_id)
#     expected_row_count = comparison.expected_table.row_count
#     actual_row_count = comparison.actual_table.row_count
#     if expected_row_count != actual_row_count:
#         report_note = "Error - different numbers of rows (Expected: %s / Actual: %s)" % (expected_row_count,
#                                                                                          actual_row_count)
#         report_notes.append(report_note)
#
#     expected_col_count = comparison.expected_table.col_count
#     actual_col_count = comparison.actual_table.col_count
#     if expected_col_count != actual_col_count:
#         report_note = "Error - different numbers of columns (Expected: %s / Actual: %s)" % (expected_col_count,
#                                                                                             actual_col_count)
#         report_notes.append(report_note)
#
#     if not comparison.tables_equivalent:
#         report_note = "Error - %s different cells; %s cells are the same" % (len(comparison.diff_cells),
#                                                                              len(comparison.same_cells))
#         report_notes.append(report_note)
#
#     cd = comparison.diff_cells.keys()[:]
#     cd.sort()
#     for cell in cd:
#         report_notes.append("[%s,%s] Expected: %s Actual: %s" %
#                             (cell[0], cell[1],
#                              comparison.expected_table.get_value(cell[0], cell[1]),
#                              comparison.actual_table.get_value(cell[0], cell[1])))
#
#     if len(report_notes) == 0:
#         report_notes.append("No differences between expected and actual tables")
#
#     table_rows = []
#     for row_index in range(comparison.max_rows):
#         table_row = []
#         for col_index in range(comparison.max_cols):
#             if (row_index, col_index) in comparison.same_cells:
#                 item = ("%s" % comparison.same_cells[(row_index, col_index)], "ok")
#             elif (row_index, col_index) in comparison.diff_cells:
#                 item = (Markup("Expected: %s<br>Actual: %s" %
#                                comparison.diff_cells[(row_index, col_index)]),
#                         "mismatch")
#             elif (row_index, col_index) in comparison.expected_table_only_cells:
#                 item = (Markup("Expected: %s<br>Actual: --missing--" %
#                                comparison.expected_table_only_cells[(row_index, col_index)]),
#                         "missing_expected")
#             elif (row_index, col_index) in comparison.actual_table_only_cells:
#                 item = (Markup("Expected: --missing--<br>Actual: %s" %
#                                comparison.actual_table_only_cells[(row_index, col_index)]),
#                         "missing_actual")
#             elif (row_index, col_index) in comparison.neither_table_cell_coords:
#                 item = ("", "padding")
#             else:
#                 raise Exception("Untreated cell: %s" % ((row_index, col_index)))
#
#             table_row.append(item)
#
#         table_rows.append(table_row)
#
#     return render_template('comparison_results.html',
#                            table_rows=table_rows,
#                            report_notes=report_notes,
#                            options=options,
#                            header_tab_classes={},
#                            comparison_id=comparison_id)

# # Perform a quick comparison between two Excel files.
# @app.route('/compare/quick', methods=['GET', 'POST'])
# def quick_compare():
#     if request.method == 'GET':
#         comparison_types = models.ComparisonType.select()
#         return render_template('quick_compare.html',
#             header_tab_classes={'quick-compare': 'active'}, comparison_types=comparison_types)
#
#     baseline_file = save_excel_file(request.files['baseline_file'], 'actual')
#     actual_file = save_excel_file(request.files['comparison_file'], 'actual')
#
#     expected_results_table = td_parsers.load_table_from_xls(get_excel_file_path(baseline_file.id))
#     actual_results_table = td_parsers.load_table_from_xls(get_excel_file_path(actual_file.id))
#
#     comparison_record = models.ComparisonType.get(models.ComparisonType.id == request.form['comparison_type'])
#     comparison = td_comparison.compare_tables(expected_results_table, actual_results_table, comparison_record.name)
#     comparison_id = td_persist.store_new_comparison(comparison)
#     td_thumbnail.create_comparison_image(comparison, comparison_id)
#
#     # Note: We could delete the files once we're done with a quick comparison.
#
#     redirect_url = url_for('show_results', comparison_id=comparison_id)
#     return redirect(redirect_url)

# Manage a baseline with the specified baseline ID.
@app.route('/baseline/manage/<int:baseline_id>', methods=['GET'])
def manage_baseline_view(baseline_id):
    baselines = models.Baseline.select()
    if baselines.count() == 0:
        return display_error('There are no baselines on the server. Please upload a baseline first.')
    return render_template('manage_baselines.html',
        header_tab_classes={'manage-baseline': 'active'}, baselines=baselines, selected_baseline=baseline_id)

@app.route('/baseline/data', methods=['POST'])
def get_baseline_grid_data():
    baseline = models.Baseline.get(models.Baseline.id == request.form['baseline_id'])
    file_path = get_excel_file_path(baseline.file)
    t = td_parsers.load_table_from_xls(file_path)
    data = []
    for row in t.rows:
        data.append(row)
    response = {"result": "ok",
                "data": data}
    return jsonify(response)

# Manage a baseline
@app.route('/baseline/manage', methods=['GET', 'POST'])
def manage_baselines():
    if request.method == 'GET':
        return manage_baseline_view(None)

    # If there are files in the request, store them.
    if request.method == 'POST':
        baseline_file = save_excel_file(request.files['baseline_file'], 'baselines')
        baseline_record = models.Baseline.create(
            name=request.form['baseline_name'],
            file=baseline_file.id,
            comparison=1
        )

    return redirect(url_for('manage_baselines'))

# Upload an Excel baseline and store it in the database.
@app.route('/baseline/upload', methods=['GET', 'POST'])
def upload_baseline():
    # If there are files in the request, store them.
    if request.method == 'POST':
        baseline_file = save_excel_file(request.files['baseline_file'], 'baselines')
        baseline_record = models.Baseline.create(
            name=request.form['baseline_name'],
            file=baseline_file.id,
            comparison=request.form['comparison_type']
        )
        return redirect(url_for('compare_baseline') + '/' + str(baseline_record.id))

    # If there are no files present, display the upload page.
    comparison_types = models.ComparisonType.select()
    return render_template('upload_baseline.html',
                               header_tab_classes={'upload-baseline': 'active'},
                               comparison_types=comparison_types)

# # Compare a file with an existing baseline.
# @app.route('/baseline/compare', methods=['GET', 'POST'])
# def compare_baseline():
#     if request.method == 'GET':
#         return compare_baseline_view(None)
#
#     baseline = models.Baseline.get(models.Baseline.id == request.form['baseline_id'])
#     baseline_path = get_excel_file_path(baseline.file)
#
#     actual_file = save_excel_file(request.files['compare_file'], 'actual')
#
#     expected_results_table = td_parsers.load_table_from_xls(baseline_path)
#     actual_results_table = td_parsers.load_table_from_xls(get_excel_file_path(actual_file.id))
#
#     # Note: Could we join here using the ORM instead?
#     comparison_record = models.ComparisonType.get(models.ComparisonType.id == baseline.comparison)
#     comparison = td_comparison.compare_tables(expected_results_table, actual_results_table, comparison_record.name)
#     comparison_id = td_persist.store_new_comparison(comparison)
#     td_thumbnail.create_comparison_image(comparison, comparison_id)
#
#     redirect_url = url_for('show_results', comparison_id=comparison_id)
#     return redirect(redirect_url)

@app.route('/baseline/compare/<int:baseline_id>', methods=['GET'])
def compare_baseline_view(baseline_id):
    baselines = models.Baseline.select()
    if baselines.count() == 0:
        return display_error('There are no baselines on the server. Please upload a baseline first.')
    return render_template('compare_baseline.html',
        header_tab_classes={'compare-baseline': 'active'}, baselines=baselines, selected_baseline=baseline_id)

def get_excel_file_path(file_id):
    file_record = models.UploadedFile.get(models.UploadedFile.id == file_id)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_record.directory, file_record.name)
    return file_path

def save_excel_file(file, directory):
    if file and allowed_file(file.filename):
        # Create a new file record object in the database.
        file_record = models.UploadedFile()
        file_record.name = ''
        file_record.directory = directory
        file_record.created = datetime.datetime.now()
        file_record.save()

        # Store the file with the file record's ID prepended to the name.
        filename = secure_filename(str(file_record.id) + '_' + file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], directory, filename))

        # Update the file record with the file's name.
        file_record.name = filename
        file_record.save()

        return file_record

    raise Exception('The file is not valid!')

@app.route('/data/new_results/<comparison_id>', methods=['GET'])
def show_new_results_data(comparison_id):
    comparison = td_persist.retrieve_results(comparison_id)

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
                items_row.append(Markup("Expected: %s<br>Actual: %s" %
                               comparison.diff_cells[(row_index, col_index)]))
                item_styles_row.append("mismatch")
            elif (row_index, col_index) in comparison.expected_table_only_cells:
                items_row.append(Markup("Expected: %s<br>Actual: --missing--" %
                               comparison.expected_table_only_cells[(row_index, col_index)]))
                item_styles_row.append("missing_expected")
            elif (row_index, col_index) in comparison.actual_table_only_cells:
                items_row.append(Markup("Expected: --missing--<br>Actual: %s" %
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

@app.route('/thumbnails/<comparison_id>', methods=['GET'])
def thumbnails(comparison_id):
    return send_from_directory(td_thumbnail.THUMBNAIL_DIR,
                               "%s.png" % comparison_id)

def display_error(error_message):
    return render_template('error.html', header_tab_classes=None, error_message=error_message)

admin.setup()
api.setup()

if __name__ == "__main__":
    app.run(host='0.0.0.0',
            port=5005,
            debug=True)