
from flask import Blueprint, render_template, abort, request, url_for, jsonify, redirect
import models, td_persist, td_parsers

blueprint = Blueprint('baselines', __name__,
                      template_folder='templates')

# Manage a baseline with the specified baseline ID.
@blueprint.route('/manage/<int:baseline_id>', methods=['GET'])
def manage_baseline_view(baseline_id):
    baselines = models.Baseline.select()
    if baselines.count() == 0:
        return display_error('There are no baselines on the server. Please upload a baseline first.')
    return render_template('manage_baselines.html',
                           header_tab_classes={'manage-baseline': 'active'},
                           baselines=baselines,
                           selected_baseline=baseline_id)

# Manage a baseline
@blueprint.route('/manage', methods=['GET', 'POST'])
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
@blueprint.route('/upload', methods=['GET', 'POST'])
def upload_baseline():
    # If there are files in the request, store them.
    if request.method == 'POST':
        baseline_file = td_persist.save_excel_file(request.files['baseline_file'], 'baselines')
        baseline_record = models.Baseline.create(
            name=request.form['baseline_name'],
            file=baseline_file.id,
            comparison=request.form['comparison_type']
        )
        # return redirect(url_for('compare_baseline') + '/' + str(baseline_record.id))
        return redirect(url_for('compare.compare_baseline_view', baseline_id=baseline_record.id))

    # If there are no files present, display the upload page.
    comparison_types = models.ComparisonType.select()
    return render_template('upload_baseline.html',
                           header_tab_classes={'upload-baseline': 'active'},
                           comparison_types=comparison_types)

# Compare a file with an existing baseline.
@blueprint.route('/compare', methods=['GET', 'POST'])
def compare_baseline():
    if request.method == 'GET':
        return compare_baseline_view(None)

    baseline = models.Baseline.get(models.Baseline.id == request.form['baseline_id'])
    baseline_path = get_excel_file_path(baseline.file)

    actual_file = save_excel_file(request.files['compare_file'], 'actual')

    expected_results_table = td_parsers.load_table_from_xls(baseline_path)
    actual_results_table = td_parsers.load_table_from_xls(get_excel_file_path(actual_file.id))

    # Note: Could we join here using the ORM instead?
    comparison_record = models.ComparisonType.get(models.ComparisonType.id == baseline.comparison)
    comparison = td_comparison.compare_tables(expected_results_table, actual_results_table, comparison_record.name)
    comparison_id = td_persist.store_new_comparison(comparison)
    td_thumbnail.create_comparison_image(comparison, comparison_id)

    redirect_url = url_for('show_results', comparison_id=comparison_id)
    return redirect(redirect_url)

@blueprint.route('/compare/<int:baseline_id>', methods=['GET'])
def compare_baseline_view(baseline_id):
    baselines = models.Baseline.select()
    if baselines.count() == 0:
        return display_error('There are no baselines on the server. Please upload a baseline first.')
    return render_template('compare_baseline.html',
                           header_tab_classes={'compare-baseline': 'active'},
                           baselines=baselines,
                           selected_baseline=baseline_id)

@blueprint.route('/data', methods=['POST'])
def get_baseline_grid_data():
    baseline = models.Baseline.get(models.Baseline.id == request.form['baseline_id'])
    file_path = td_persist.get_excel_file_path(baseline.file)
    t = td_parsers.load_table_from_xls(file_path)
    data = []
    for row in t.rows:
        data.append(row)
    response = {"result": "ok",
                "data": data}
    return jsonify(response)
