import datetime
import pickle

from flask import Blueprint, render_template, request, url_for, jsonify, redirect
import models
import td_persist
import td_parsers
import td_file
import compare
import table_comparisons
import cell_comparisons
import td_baseline


blueprint = Blueprint('baselines', __name__,
                      template_folder='templates')

# View all baselines
@blueprint.route('/')
def list_baselines():
    baselines = models.Baseline.select()
    return render_template('list_baselines.html',
                           header_tab_classes={'manage-baseline': 'active'},
                           baselines=baselines,
                           )

    return redirect(url_for('list_baselines'))

# Manage a baseline with the specified baseline ID.
@blueprint.route('/<int:baseline_id>')
def view_baseline(baseline_id):
    baseline = models.Baseline.get(models.Baseline.id == baseline_id)
    comparison_operations = cell_comparisons.CHOICES

    return render_template('show_baseline.html',
                           header_tab_classes={'manage-baseline': 'active'},
                           baseline=baseline,
                           comparison=baseline.default_cell_comparison_type,
                           comparison_operations=comparison_operations,
                           selected_baseline=baseline_id)

# Manage a baseline with the specified baseline ID.
@blueprint.route('/<int:baseline_id>', methods=['POST'])
def update_baseline(baseline_id):
    baseline = models.Baseline.get(models.Baseline.id == baseline_id)

    baseline_name = request.json['baselineName']
    comparison_type = int(request.json['comparisonType'])
    table_data = td_parsers.load_table_from_handson_json(request.json['table'])
    comparison_classes = request.json['comparison_classes']

    new_td_baseline_grid = make_baseline_from_table_and_comparison_classes(table_data, comparison_classes)

    baseline.pickled_td_baseline_grid = pickle.dumps(new_td_baseline_grid)
    baseline.name = baseline_name
    baseline.default_cell_comparison_type = comparison_type
    baseline.save()

    redirect_url = url_for('baselines.view_baseline',
                           baseline_id=baseline.id)
    return jsonify(redirect_url=redirect_url)


# Upload an Excel baseline and store it in the database.
@blueprint.route('/upload', methods=['GET', 'POST'])
def upload_baseline():
    if request.method == 'POST':
        baseline_file = td_file.save_excel_file(request.files['baseline_file'], 'baselines')
        baseline_table = td_parsers.load_table_from_xls(baseline_file)

        now = datetime.datetime.now()

        comparison_operation = int(request.form['comparison_type'])
        baseline_name = request.form['baseline_name'].strip()
        if len(baseline_name) < 1:
            baseline_name = "File upload at %s" % now

        table_comparison = table_comparisons.RowByRowTableComparison()

        baseline = models.Baseline.create(
            name=baseline_name,
            description="Uploaded by user on %s" % now,
            default_cell_comparison_type=comparison_operation,
            pickled_td_baseline_grid=pickle.dumps(baseline_table),
            pickled_td_table_comparison=pickle.dumps(table_comparison),
            last_modified=now,
            created=now,
            adhoc=False,
            )

        return redirect(url_for('baselines.compare_baseline',
                                baseline_id=baseline.id))

    # If there are no files present, display the upload page.
    return render_template('upload_baseline.html',
                           header_tab_classes={'upload-baseline': 'active'},
                           comparison_operations=cell_comparisons.CHOICES)

# Compare a file with an existing baseline.
@blueprint.route('/compare', methods=['GET', 'POST'])
def compare_baselines():
    if request.method == 'GET':
        return compare_baseline(None)

    baseline_id = request.form['baseline_id']
    return compare_baseline(baseline_id)

@blueprint.route('/<int:baseline_id>/compare', methods=['GET', 'POST'])
def compare_baseline(baseline_id):
    if request.method == 'GET':
        baselines = models.Baseline.select()
        if baselines.count() == 0:
            return display_error('There are no baselines on the server. Please upload a baseline first.')
        return render_template('compare_baseline.html',
                               header_tab_classes={'compare-baseline': 'active'},
                               baselines=baselines,
                               selected_baseline=baseline_id)

    actual_file = td_file.save_excel_file(request.files['compare_file'], 'actual')
    actual_results_table = td_parsers.load_table_from_xls(actual_file)

    comparison = compare.do_baseline_comparison(actual_results_table,
                                                baseline_id)

    redirect_url = url_for('results.show_result',
                           comparison_id=comparison.id)
    return redirect(redirect_url)

@blueprint.route('/<int:baseline_id>/data')
def get_baseline_grid_data(baseline_id):
    baseline = models.Baseline.get(models.Baseline.id == baseline_id)
    baseline_grid = pickle.loads(baseline.pickled_td_baseline_grid)
    data = []
    comparison_classes = []
    for row in baseline_grid.rows:
        data_row = []
        comparison_row = []
        for cell in row:
            data_row.append("%s" % cell)
            comparison_row.append(cell.comparison_class)
        data.append(data_row)
        comparison_classes.append(comparison_row)

    response = {"result": "ok",
                "data": data,
                "comparison_classes": comparison_classes}
    return jsonify(response)

def display_error(error_message):
    return render_template('error.html',
                           header_tab_classes=None,
                           error_message=error_message)


def make_baseline_from_table_and_comparison_classes(table, comparison_classes):
    baseline_grid = td_baseline.TdBaselineGrid()
    for value_row, class_row in zip(table.rows, comparison_classes):
        cmp_row = []
        for cell_value, cell_class in zip(value_row, class_row):
            cell_comparison_class = cell_comparisons.get_constructor_for_comparison_class(cell_class)
            cmp = cell_comparison_class(cell_value)
            cmp_row.append(cmp)
        baseline_grid.add_row(cmp_row)

    return baseline_grid
