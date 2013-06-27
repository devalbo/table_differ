import compare_data
import os
import models
import td_config
import td_parsers
import td_persist
import td_comparison
import datetime

import flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from flask import Markup
from flask import send_from_directory

from werkzeug import secure_filename

from app import app

ALLOWED_EXTENSIONS = set(['xls', 'xlsx', 'csv'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/copy-paste-compare', methods=['GET', 'POST'])
def copy_paste_compare():
    if request.method == 'GET':
        return render_template('new_tables_input.html',
                               header_tab_classes={'copy-paste-compare': 'active'})

    table1 = td_parsers.load_table_from_handson_json(request.json['dataTable1'])
    table2 = td_parsers.load_table_from_handson_json(request.json['dataTable2'])

    comparison = compare_data.compare_tables(table1, table2, td_comparison.COMPARE_LITERAL)
    comparison_id = td_persist.store_new_comparison(comparison)

    redirect_url = url_for('show_new_results', comparison_id=comparison_id)
    return flask.jsonify(redirect_url=redirect_url)

# Does this work?
@app.route('/file-compare', methods=['GET', 'POST'])
def file_compare():
    if request.method == 'GET':
        return render_template('file_compare.html',
                               header_tab_classes={'file-compare': 'active'})

    actual_results_file = request.files['actual_results']
    expected_results_file = request.files['expected_results']
    for results_file in (actual_results_file, expected_results_file):
        if results_file and allowed_file(results_file.filename):
            filename = secure_filename(results_file.filename)
            results_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for('file_compare'))

@app.route('/xls-worksheet-compare', methods=['GET', 'POST'])
def xls_worksheet_compare():
    if request.method == 'GET':
        return render_template('xls_worksheet_compare.html',
                               header_tab_classes={'xls-worksheet-compare': 'active'})

    worksheet_results_file = request.files['worksheet_file']
    if worksheet_results_file and allowed_file(worksheet_results_file.filename):
        filename = secure_filename(worksheet_results_file.filename)
        file_location = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        worksheet_results_file.save(file_location)

        expected_worksheet_name = "Reference"
        actual_worksheet_name = "Actual"

        expected_results_table = td_parsers.load_table_from_xls(file_location, expected_worksheet_name)
        actual_results_table = td_parsers.load_table_from_xls(file_location, actual_worksheet_name)

        comparison = compare_data.compare_tables(expected_results_table, actual_results_table, td_comparison.COMPARE_RE_SKIP)
        comparison_id = td_persist.store_new_comparison(comparison)

        redirect_url = url_for('show_new_results', comparison_id=comparison_id)
        return redirect(redirect_url)

    return redirect(url_for('xls_worksheet_compare'))

@app.route('/compare', methods=['GET', 'POST'])
def compare():
    if request.method == 'GET':
        return render_template('full_compare.html',
                               header_tab_classes={'table-compare': 'active'})

@app.route('/manage-tables', methods=['GET', 'POST'])
def manage_tables():
    if request.method == 'GET':
        return render_template('manage-tables.html',
                               header_tab_classes={'manage-tables': 'active'})

@app.route('/new_results/<comparison_id>', methods=['GET'])
def show_new_results(comparison_id):
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

    for cell in comparison.diff_cells:
        report_notes.append("[%s,%s] Expected: %s Actual: %s" %
                            (cell[0], cell[1],
                             comparison.expected_table.get_value(cell[0], cell[1]),
                             comparison.actual_table.get_value(cell[0], cell[1])))

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

    return render_template('data_comparison_new_results.html',
                           table_rows=table_rows,
                           report_notes=report_notes,
                           options=options,
                           header_tab_classes={})

@app.route('/uploads', methods=['GET', 'POST'])
def uploads():
    if request.method == 'POST':
        file1 = request.files['file1']
        if file1 and allowed_file(file1.filename):
            filename = secure_filename(file1.filename)
            file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template("uploads.html")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

# Upload an Excel baseline and store it in the database.
@app.route('/upload/baseline', methods=['GET', 'POST'])
def upload_baseline():
    # If there are files in the request, store them.
    if request.method == 'POST':
        baseline_file = save_excel_file(request.files['baseline_file'], 'baselines')
        baseline_record = models.Baseline.create(
            name=request.form['baseline_name'],
            file=baseline_file.id,
            comparison=1
        )
        return redirect(url_for('compare_baseline'))

    # If there are no files present, display the upload page.
    return render_template('upload_baseline.html',
                               header_tab_classes={'upload-baseline': 'active'})

# Compare a file with an existing baseline.
@app.route('/compare/baseline', methods=['GET', 'POST'])
def compare_baseline():
    if request.method == 'GET':
        baselines = models.Baseline.select()
        if baselines.count() == 0:
            return 'No baselines exist :('
        comparison_types = models.ComparisonType.select()
        return render_template('compare_baseline.html',
            header_tab_classes={'compare-baseline': 'active'}, baselines=baselines, comparison_types=comparison_types)

    baseline_id = request.form['baseline_id']
    baseline = models.Baseline.get(models.Baseline.id == baseline_id)
    baseline_path = get_excel_file_path(baseline.file)

    actual_file = save_excel_file(request.files['compare_file'], 'actual')

    expected_results_table = td_parsers.load_table_from_xls(baseline_path)
    actual_results_table = td_parsers.load_table_from_xls(get_excel_file_path(actual_file.id))

    comparison_type = models.ComparisonType.get(models.ComparisonType.id == request.form['comparison_type'])
    comparison = compare_data.compare_tables(expected_results_table, actual_results_table, comparison_type.name)
    comparison_id = td_persist.store_new_comparison(comparison)

    redirect_url = url_for('show_new_results', comparison_id=comparison_id)
    return redirect(redirect_url)

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

@app.route('/test_sheet')
def test_sheet():
    return render_template('test_sheet.html',
                           header_tab_classes={'compare-baseline': 'active'})

@app.route('/test_sheet_data', methods=['GET', 'POST'])
def test_sheet_data():
    if request.method == 'GET':
        t = td_parsers.load_table_from_xls('test_sheet.xls', 'MainSheet')
        data = []
        for row in t.rows:
            data.append(row)
        response = {"result": "ok",
                    "data": data}
        return flask.jsonify(response)

    # if request.method == 'POST':
    #     baseline_file = save_excel_file(request.files['baseline_file'], 'baselines')




if __name__ == "__main__":
    app.run(host='0.0.0.0',
            port=5005,
            debug=True)