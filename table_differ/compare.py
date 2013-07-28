
import datetime, pickle
from flask import Blueprint, render_template, abort, request, url_for, jsonify, Markup, redirect
import models, td_parsers, td_comparison, td_persist, baselines, td_file, td_baseline, cell_comparisons, table_comparisons
from collections import OrderedDict

try:
    import td_thumbnail
except ImportError, e:
    print "Image support isn't available - thumbnail/image results won't be supported"


blueprint = Blueprint('compare', __name__,
                      template_folder='templates')

# @blueprint.route('/copy-paste', methods=['GET', 'POST'])
# def copy_paste_compare():
#     if request.method == 'GET':
#         return render_template('tables_input.html',
#                                header_tab_classes={'copy-paste-compare': 'active'})
#
#     actual_table = td_parsers.load_table_from_handson_json(request.json['actualTable'])
#     expected_table = td_parsers.load_table_from_handson_json(request.json['expectedTable'])
#     comparison_id = do_adhoc_comparison(actual_table,
#                                         expected_table,
#                                         td_comparison.COMPARE_LITERAL,
#                                         "Quick compare at %s" % datetime.datetime.now())
#
#     redirect_url = url_for('results.show_result',
#                            comparison_id=comparison_id)
#     return jsonify(redirect_url=redirect_url)

@blueprint.route('/copy-paste', methods=['GET', 'POST'])
def copy_paste_compare():
    if request.method == 'GET':
        return render_template('tables_input.html',
                               header_tab_classes={'copy-paste-compare': 'active'})

    expected_table = td_parsers.load_table_from_handson_json(request.json['expectedTable'])
    baseline = make_baseline(expected_table,
                             cell_comparisons.LiteralCellComparison.comparison_name)

    actual_table = td_parsers.load_table_from_handson_json(request.json['actualTable'])
    comparison = do_baseline_comparison(actual_table, baseline.id)

    # comparison_id = do_adhoc_comparison(actual_table,
    #                                     expected_table,
    #                                     cell_comparisons.LiteralCellComparison.comparison_name,
    #                                     "Quick compare at %s" % datetime.datetime.now())

    redirect_url = url_for('results.show_result',
                           comparison_id=comparison.id)
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
        baseline = make_baseline(expected_results_table,
                                 cell_comparisons.LiteralCellComparison.comparison_name)

        actual_results_table = td_parsers.load_table_from_xls(file_location, actual_worksheet_name)
        comparison = do_baseline_comparison(actual_results_table, baseline.id)

        # comparison_id = td_comparison.do_adhoc_comparison(expected_results_table,
        #                                                   actual_results_table,
        #                                                   td_comparison.COMPARE_RE_SKIP)

        redirect_url = url_for('results.show_result',
                               comparison_id=comparison.id)
        return redirect(redirect_url)

    return redirect(url_for('compare.xls_worksheet_compare'))

# # Perform a quick comparison between two Excel files.
# @blueprint.route('/quick', methods=['GET', 'POST'])
# def quick_compare():
#     if request.method == 'GET':
#         return render_template('quick_compare.html',
#                                header_tab_classes={'quick-compare': 'active'},
#                                comparison_operations=models.ComparisonOperation.CHOICES)
#
#     baseline_file = td_file.save_excel_file(request.files['baseline_file'], 'actual')
#     actual_file = td_file.save_excel_file(request.files['comparison_file'], 'actual')
#
#     expected_results_table = td_parsers.load_table_from_xls(baseline_file)
#     actual_results_table = td_parsers.load_table_from_xls(actual_file)
#
#     comparison_operation = models.ComparisonOperation.CHOICES[int(request.form['comparison_type'])]
#     comparison_id = do_old_adhoc_comparison(expected_results_table,
#                                             actual_results_table,
#                                             comparison_operation)
#
#     redirect_url = url_for('results.show_result',
#                            comparison_id=comparison_id)
#     return redirect(redirect_url)

# Perform a quick comparison between two Excel files.
@blueprint.route('/quick', methods=['GET', 'POST'])
def quick_compare():
    if request.method == 'GET':
        return render_template('quick_compare.html',
                               header_tab_classes={'quick-compare': 'active'},
                               comparison_operations=cell_comparisons.CHOICES)

    baseline_file = td_file.save_excel_file(request.files['baseline_file'], 'actual')
    actual_file = td_file.save_excel_file(request.files['comparison_file'], 'actual')

    comparison_operation = cell_comparisons.CHOICES[int(request.form['comparison_type'])]
    expected_results_table = td_parsers.load_table_from_xls(baseline_file)
    baseline = make_baseline(expected_results_table,
                             comparison_operation)

    actual_results_table = td_parsers.load_table_from_xls(actual_file)
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

# def do_old_baseline_comparison(actual_results_table,
#                            baseline_id,
#                            timestamp=datetime.datetime.now(),
#                            description="Baseline comparison"):
#
#     baseline = models.OldBaseline.get(models.OldBaseline.id == baseline_id)
#     expected_results_table = pickle.loads(baseline.pickled_expected_table)
#     comparison_type = baseline.comparison_operation.name
#
#     comparison = td_comparison.compare_tables(expected_results_table,
#                                               actual_results_table,
#                                               comparison_type)
#     try:
#         thumbnail_img = td_thumbnail.create_comparison_image(comparison)
#     except NameError, e:
#         thumbnail_img = ""
#
#     comparison_result = models.ComparisonResult.create(
#         pickled_actual_table=pickle.dumps(actual_results_table),
#         baseline=baseline,
#         comparison_image=thumbnail_img,
#         pickled_comparison_report=pickle.dumps(comparison),
#         timestamp=timestamp,
#         )
#
#     return comparison_result.id
#
# def do_old_adhoc_comparison(actual_table, expected_table, comparator,
#                         baseline_name="New baseline",
#                         baseline_description="Ad hoc comparison"):
#
#     now = datetime.datetime.now()
#
#     comparison_type = -1
#     for k, v in models.ComparisonOperation.CHOICES.items():
#         if comparator == v:
#             comparison_type = k
#
#     if comparison_type < 0:
#         raise Exception("No such comparator: %s" % comparator)
#
#     literal_compare = models.create_comparison_operation(comparison_type)
#     baseline = models.OldBaseline.create(
#         name=baseline_name,
#         description=baseline_description,
#         pickled_expected_table=pickle.dumps(expected_table),
#         comparison_operation=literal_compare,
#         last_modified=now,
#         created=now,
#         adhoc=True,
#         )
#
#     return do_old_baseline_comparison(actual_table, baseline.id)


def do_baseline_comparison(actual_results_table,
                           baseline_id,
                           timestamp=datetime.datetime.now(),
                           description="Baseline comparison"):

    baseline = models.Baseline.get(models.Baseline.id == baseline_id)
    baseline_grid = pickle.loads(baseline.pickled_td_baseline_grid)
    table_comparison = pickle.loads(baseline.pickled_td_table_comparison)
    # comparison_type = baseline.default_cell_comparison

    comparison = table_comparison.compare_table_to_baseline_grid(actual_results_table,
                                                                 baseline_grid)
    try:
        thumbnail_img = td_thumbnail.create_comparison_image(comparison)
    except NameError, e:
        thumbnail_img = ""

    comparison_result = models.ComparisonResult.create(
        pickled_actual_table=pickle.dumps(actual_results_table),
        pickled_comparison_report=pickle.dumps(comparison),
        baseline=baseline,
        comparison_image=thumbnail_img,
        timestamp=timestamp,
        )

    return comparison_result


# def do_adhoc_comparison(actual_table,
#                         expected_table,
#                         cell_comparison_name,
#                         table_comparison_name,
#                         baseline_name="New baseline",
#                         baseline_description="Ad hoc comparison"):
#
#     now = datetime.datetime.now()
#
#     cell_comparison_type = -1
#     for k, v in cell_comparisons.CHOICES.items():
#         if cell_comparison_name == v:
#             cell_comparison_type = k
#
#     if cell_comparison_type < 0:
#         raise Exception("No such cell comparison name: %s" % cell_comparison_name)
#
#     cell_comp_type_name = cell_comparisons.CHOICES[cell_comparison_type]
#     cell_comp_instance_class = cell_comparisons._CELL_COMPARISONS[cell_comp_type_name]
#     baseline_grid = td_baseline.make_baseline_grid_from_table(expected_table, cell_comp_instance_class)
#
#     table_comp_type_name = table_comparisons.CHOICES[table_comparison_name]
#     table_comp_instance_class = table_comparisons._TABLE_COMPARISONS[table_comp_type_name]
#     table_comparison = table_comp_instance_class()
#     #
#     # table_comparison = table_comparisons.RowByRowTableComparison()
#
#     baseline = models.Baseline.create(
#         name=baseline_name,
#         description=baseline_description,
#         pickled_td_baseline_grid=pickle.dumps(baseline_grid),
#         pickled_td_table_comparison=pickle.dumps(table_comparison),
#         default_cell_comparison_type=cell_comparison_type,
#         last_modified=now,
#         created=now,
#         adhoc=True,
#         )
#
#     return do_baseline_comparison(actual_table, baseline.id)


def make_baseline(expected_table,
                  cell_comparison_name,
                  table_comparison_name="Row by row comparison",
                  baseline_name="New baseline",
                  baseline_description="Ad hoc comparison"):
    now = datetime.datetime.now()

    cell_comparison_type = -1
    for k, v in cell_comparisons.CHOICES.items():
        if cell_comparison_name == v:
            cell_comparison_type = k

    if cell_comparison_type < 0:
        raise Exception("No such cell comparison name: %s" % cell_comparison_name)

    cell_comp_type_name = cell_comparisons.CHOICES[cell_comparison_type]
    cell_comp_instance_class = cell_comparisons._CELL_COMPARISONS[cell_comp_type_name]
    baseline_grid = td_baseline.make_baseline_grid_from_table(expected_table, cell_comp_instance_class)

    table_comparison_type = -1
    for k, v in table_comparisons.CHOICES.items():
        if table_comparison_name == v:
            table_comparison_type = k

    table_comp_type_name = table_comparisons.CHOICES[table_comparison_type]
    table_comp_instance_class = table_comparisons._TABLE_COMPARISONS[table_comp_type_name]
    table_comparison = table_comp_instance_class()
    #
    # table_comparison = table_comparisons.RowByRowTableComparison()

    baseline = models.Baseline.create(
        name=baseline_name,
        description=baseline_description,
        pickled_td_baseline_grid=pickle.dumps(baseline_grid),
        pickled_td_table_comparison=pickle.dumps(table_comparison),
        default_cell_comparison_type=cell_comparison_type,
        last_modified=now,
        created=now,
        adhoc=True,
        )

    return baseline