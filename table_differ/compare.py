
import datetime, pickle
from flask import Blueprint, render_template, abort, request, url_for, jsonify, Markup, redirect
import models, td_parsers, td_comparison, td_persist, baselines, td_file
try:
    import td_thumbnail
except ImportError, e:
    print "Image support isn't available - thumbnail/image results won't be supported"


blueprint = Blueprint('compare', __name__,
                      template_folder='templates')

@blueprint.route('/copy-paste', methods=['GET', 'POST'])
def copy_paste_compare():
    if request.method == 'GET':
        return render_template('tables_input.html',
                               header_tab_classes={'copy-paste-compare': 'active'})

    actual_table = td_parsers.load_table_from_handson_json(request.json['actualTable'])
    expected_table = td_parsers.load_table_from_handson_json(request.json['expectedTable'])
    comparison_id = td_comparison.do_adhoc_comparison(actual_table, expected_table, td_comparison.COMPARE_LITERAL,
                                                      "Quick compare at %s" % datetime.datetime.now())

    redirect_url = url_for('results.show_result',
                           comparison_id=comparison_id)
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

        comparison_id = _do_adhoc_comparison(expected_results_table, actual_results_table, td_comparison.COMPARE_RE_SKIP)

        redirect_url = url_for('results.show_result',
                               comparison_id=comparison_id)
        return redirect(redirect_url)

    return redirect(url_for('compare.xls_worksheet_compare'))

# Perform a quick comparison between two Excel files.
@blueprint.route('/quick', methods=['GET', 'POST'])
def quick_compare():
    if request.method == 'GET':
        return render_template('quick_compare.html',
                               header_tab_classes={'quick-compare': 'active'},
                               comparison_operations=models.ComparisonOperation.CHOICES)

    baseline_file = td_file.save_excel_file(request.files['baseline_file'], 'actual')
    actual_file = td_file.save_excel_file(request.files['comparison_file'], 'actual')

    expected_results_table = td_parsers.load_table_from_xls(baseline_file)
    actual_results_table = td_parsers.load_table_from_xls(actual_file)


    comparison_operation = models.ComparisonOperation.CHOICES_DICT[int(request.form['comparison_type'])]
    comparison_id = td_comparison.do_adhoc_comparison(expected_results_table, actual_results_table, comparison_operation)

    redirect_url = url_for('results.show_result',
                           comparison_id=comparison_id)
    return redirect(redirect_url)

@blueprint.route('/baseline/')
def compare_baseline():
    redirect_url = url_for('baselines.compare_baselines')
    return redirect(redirect_url)

@blueprint.route('/baseline/<int:baseline_id>')
def compare_baseline_view(baseline_id):
    redirect_url = url_for('baselines.compare_baseline', baseline_id=baseline_id)
    return redirect(redirect_url)

