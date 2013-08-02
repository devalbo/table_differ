
import os
import datetime, json
from flask import Blueprint, render_template, request, url_for, jsonify, redirect
from werkzeug import secure_filename

import models, td_parsers, td_file, td_baseline, cell_comparisons, table_comparisons
from app import app

try:
    import td_thumbnail
except ImportError, e:
    print "Image support isn't available - thumbnail/image results won't be supported"


blueprint = Blueprint('compare', __name__,
                      template_folder='templates')


ALLOWED_EXTENSIONS = set(['xls', 'xlsx', 'csv'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@blueprint.route('/copy-paste', methods=['GET', 'POST'])
def copy_paste_compare():
    if request.method == 'GET':
        return render_template('tables_input.html',
                               header_tab_classes={'copy-paste-compare': 'active'})

    expected_table = td_parsers.load_table_from_handson_json(request.json['expectedTable'])
    baseline_name = "Copy/paste comparison baseline @ %s" % datetime.datetime.now().strftime('%Y-%m-%d %I:%M %p')
    baseline = make_baseline(expected_table,
                             cell_comparisons.LiteralCellComparison.comparison_type_id,
                             baseline_name=baseline_name)

    actual_table = td_parsers.load_table_from_handson_json(request.json['actualTable'])
    comparison = do_baseline_comparison(actual_table, baseline.id)

    redirect_url = url_for('results.show_result',
                           comparison_id=comparison.id)
    return jsonify(redirect_url=redirect_url)

@blueprint.route('/actref-file', methods=['GET', 'POST'])
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
        baseline = make_baseline(expected_results_table,
                                 cell_comparisons.LiteralCellComparison.comparison_name)

        actual_results_table = td_parsers.load_table_from_xls(file_location, actual_worksheet_name)
        comparison = do_baseline_comparison(actual_results_table, baseline.id)

        redirect_url = url_for('results.show_result',
                               comparison_id=comparison.id)
        return redirect(redirect_url)

    return redirect(url_for('compare.xls_worksheet_compare'))

# Perform a quick comparison between two Excel files.
@blueprint.route('/file-file', methods=['GET', 'POST'])
def quick_compare():
    if request.method == 'GET':
        return render_template('quick_compare.html',
                               header_tab_classes={'quick-compare': 'active'},
                               cell_comparisons=cell_comparisons)

    expected_results_table = td_file.load_table_from_file_upload(request.files['baseline_file'])
    comparison_type_id = int(request.form['comparison_type_id'])
    baseline_name = "File comparison baseline @ %s" % datetime.datetime.now().strftime('%Y-%m-%d %I:%M %p')

    baseline = make_baseline(expected_results_table,
                             comparison_type_id,
                             baseline_name=baseline_name)

    actual_results_table = td_file.load_table_from_file_upload(request.files['comparison_file'])
    comparison = do_baseline_comparison(actual_results_table, baseline.id)

    redirect_url = url_for('results.show_result',
                           comparison_id=comparison.id)
    return redirect(redirect_url)

@blueprint.route('/baseline/')
def compare_baseline():
    redirect_url = url_for('baselines.compare_baselines')
    return redirect(redirect_url)

@blueprint.route('/baseline/<int:baseline_id>')
def compare_baseline_view(baseline_id):
    redirect_url = url_for('baselines.compare_baseline', baseline_id=baseline_id)
    return redirect(redirect_url)

def do_baseline_comparison(actual_table,
                           baseline_id,
                           timestamp=datetime.datetime.now(),
                           description="Baseline comparison"):

    baseline = models.Baseline.get(models.Baseline.id == baseline_id)
    baseline_grid = td_baseline.make_baseline_grid_from_json(baseline.td_baseline_grid_json)
    table_comparison = table_comparisons.create_comparison_from_json(baseline.td_table_comparison_json)

    comparison = table_comparison.compare_table_to_baseline_grid(actual_table,
                                                                 baseline_grid)
    try:
        thumbnail_img = td_thumbnail.create_comparison_image(comparison)
    except NameError, e:
        thumbnail_img = ""

    comparison_result = models.ComparisonResult.create(
        actual_table_csv=actual_table.to_csv_str(),
        baseline=baseline,
        comparison_image=thumbnail_img,
        timestamp=timestamp,
        )

    return comparison_result

def make_baseline(expected_table,
                  cell_comparison_type,
                  table_comparison_type_id=table_comparisons.RowByRowTableComparison.comparison_type_id,
                  baseline_name="New baseline",
                  baseline_description="Ad hoc comparison"):
    now = datetime.datetime.now()

    # cell_comparison_type = -1
    # for k, v in cell_comparisons.:
    #     if cell_comparison_type == v:
    #         cell_comparison_type = k
    #
    # if cell_comparison_type < 0:
    #     raise Exception("No such cell comparison type: %s" % cell_comparison_name)

    # cell_comp_type_name = cell_comparisons.CHOICES[cell_comparison_type][1]
    cell_comp_instance_class = cell_comparisons.CELL_COMPARISONS[cell_comparison_type]
    baseline_grid = td_baseline.make_baseline_grid_from_table(expected_table, cell_comp_instance_class)

    # table_comparison_type = -1
    # for k, v in table_comparisons.CHOICES:
    #     if table_comparison_name == v:
    #         table_comparison_type = k

    table_comp_instance_class = table_comparisons.TABLE_COMPARISONS[table_comparison_type_id]
    table_comparison = table_comp_instance_class()

    baseline = models.Baseline.create(
        name=baseline_name,
        description=baseline_description,
        td_baseline_grid_json=baseline_grid.to_json(),
        td_table_comparison_json=table_comparisons.get_json_for_comparison(table_comparison),
        default_cell_comparison_type=cell_comparison_type,
        last_modified=now,
        created=now,
        adhoc=True,
        )

    return baseline