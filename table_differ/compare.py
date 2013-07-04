
from flask import Blueprint, render_template, abort, request, url_for, jsonify, Markup, redirect
import models, td_parsers, td_comparison, td_persist, td_thumbnail, baselines

blueprint = Blueprint('compare', __name__,
                      template_folder='templates')

@blueprint.route('/')
@blueprint.route('/copy-paste', methods=['GET', 'POST'])
def copy_paste_compare():
    if request.method == 'GET':
        return render_template('tables_input.html',
                               header_tab_classes={'copy-paste-compare': 'active'})

    table1 = td_parsers.load_table_from_handson_json(request.json['dataTable1'])
    table2 = td_parsers.load_table_from_handson_json(request.json['dataTable2'])

    comparison = td_comparison.compare_tables(table1, table2, td_comparison.COMPARE_LITERAL)
    comparison_id = td_persist.store_new_comparison(comparison)
    td_thumbnail.create_comparison_image(comparison, comparison_id)

    redirect_url = url_for('results.show_results', comparison_id=comparison_id)
    return jsonify(redirect_url=redirect_url)

@blueprint.route('/xls-worksheet', methods=['GET', 'POST'])
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

        comparison = td_comparison.compare_tables(expected_results_table, actual_results_table, td_comparison.COMPARE_RE_SKIP)
        comparison_id = td_persist.store_new_comparison(comparison)
        td_thumbnail.create_comparison_image(comparison, comparison_id)

        redirect_url = url_for('results.show_results', comparison_id=comparison_id)
        return redirect(redirect_url)

    return redirect(url_for('xls_worksheet_compare'))

# Perform a quick comparison between two Excel files.
@blueprint.route('/quick', methods=['GET', 'POST'])
def quick_compare():
    if request.method == 'GET':
        comparison_types = models.ComparisonType.select()
        return render_template('quick_compare.html',
            header_tab_classes={'quick-compare': 'active'}, comparison_types=comparison_types)

    baseline_file = save_excel_file(request.files['baseline_file'], 'actual')
    actual_file = save_excel_file(request.files['comparison_file'], 'actual')

    expected_results_table = td_parsers.load_table_from_xls(get_excel_file_path(baseline_file.id))
    actual_results_table = td_parsers.load_table_from_xls(get_excel_file_path(actual_file.id))

    comparison_record = models.ComparisonType.get(models.ComparisonType.id == request.form['comparison_type'])
    comparison = td_comparison.compare_tables(expected_results_table, actual_results_table, comparison_record.name)
    comparison_id = td_persist.store_new_comparison(comparison)
    td_thumbnail.create_comparison_image(comparison, comparison_id)

    # Note: We could delete the files once we're done with a quick comparison.

    redirect_url = url_for('results.show_results', comparison_id=comparison_id)
    return redirect(redirect_url)

@blueprint.route('/baseline/')
def compare_baseline():
    redirect_url = url_for('baselines.compare_baseline')
    return redirect(redirect_url)

@blueprint.route('/baseline/<int:baseline_id>')
def compare_baseline_view(baseline_id):
    redirect_url = url_for('baselines.compare_baseline_view', baseline_id=baseline_id)
    return redirect(redirect_url)

