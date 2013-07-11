
import datetime, pickle
from flask import Blueprint, render_template, abort, request, url_for, jsonify, redirect
import models, td_persist, td_parsers, td_file, td_comparison, compare, td_thumbnail

blueprint = Blueprint('baselines', __name__,
                      template_folder='templates')

# View all baselines
@blueprint.route('/', methods=['GET', 'POST'])
def list_baselines():
    baselines = models.Baseline.select()
    if request.method == 'GET':
        return render_template('list_baselines.html',
                               header_tab_classes={'manage-baseline': 'active'},
                               baselines=baselines,
                               )

    # If there are files in the request, store them.
    if request.method == 'POST':
        baseline_file = td_persist.save_excel_file(request.files['baseline_file'], 'baselines')
        baseline_record = models.Baseline.create(
            name=request.form['baseline_name'],
            file=baseline_file.id,
            comparison=1
        )

    return redirect(url_for('list_baselines'))

# Manage a baseline with the specified baseline ID.
@blueprint.route('/<int:baseline_id>')
def view_baseline(baseline_id):
    baseline = models.Baseline.get(models.Baseline.id == baseline_id)
    comparison_operations = models.ComparisonOperation.CHOICES

    return render_template('show_baseline.html',
                           header_tab_classes={'manage-baseline': 'active'},
                           baseline=baseline,
                           comparison=baseline.comparison_operation.type,
                           comparison_operations=comparison_operations,
                           selected_baseline=baseline_id)

# Manage a baseline with the specified baseline ID.
@blueprint.route('/<int:baseline_id>', methods=['POST'])
def update_baseline(baseline_id):
    baseline = models.Baseline.get(models.Baseline.id == baseline_id)
    # if baselines.count() == 0:
    #     return display_error('There are no baselines on the server. Please upload a baseline first.')

    baseline_name = request.json['baselineName']
    comparison_type = request.json['comparisonType']
    table_data = td_parsers.load_table_from_handson_json(request.json['table'])

    baseline.pickled_expected_table = pickle.dumps(table_data)
    baseline.name = baseline_name
    baseline.comparison_operation.type = int(comparison_type)
    baseline.comparison_operation.save()
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

        comparison_operation = models.ComparisonOperation.create(
            type=comparison_operation,
        )

        baseline_source = models.BaselineSource.create(
            adhoc=False,
            description="Uploaded by user on %s" % now,
            )

        baseline = models.Baseline.create(
            name=baseline_name,
            pickled_expected_table=pickle.dumps(baseline_table),
            comparison_operation=comparison_operation,
            last_modified=now,
            created=now,
            source=baseline_source,
            )

        return redirect(url_for('baselines.compare_baseline',
                                baseline_id=baseline.id))

    # If there are no files present, display the upload page.
    return render_template('upload_baseline.html',
                           header_tab_classes={'upload-baseline': 'active'},
                           comparison_operations=models.ComparisonOperation.CHOICES)

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

    comparison_id = td_comparison.do_baseline_comparison(actual_results_table,
                                                         baseline_id)

    redirect_url = url_for('results.show_result',
                           comparison_id=comparison_id)
    return redirect(redirect_url)

@blueprint.route('/<int:baseline_id>/data')
def get_baseline_grid_data(baseline_id):
    baseline = models.Baseline.get(models.Baseline.id == baseline_id)
    t = pickle.loads(baseline.pickled_expected_table)
    data = []
    for row in t.rows:
        data.append(row)
    response = {"result": "ok",
                "data": data}
    return jsonify(response)

def display_error(error_message):
    return render_template('error.html',
                           header_tab_classes=None,
                           error_message=error_message)
