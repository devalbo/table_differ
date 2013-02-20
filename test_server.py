
import verify_lists as vl
import compare_data

from flask import Flask
from flask import render_template
from flask import request
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verify_lists', methods=['GET', 'POST'])
def verify_lists():
    if request.method == 'GET':
        return render_template('verify_lists.html')

    expected_list = request.form['expected_list']
    actual_list = request.form['actual_list']
    compare_type = request.form['compare_type']
    log_file_name = get_log_file_name()
    vl.init_logging(log_file_name)
    results = vl.verify_lists(expected_list, actual_list,
                              compare_type, True)
    vl.stop_logging
    f = open(log_file_name)
    contents = f.read()
    f.close()

    return render_template('verify_lists_results.html',
                           content=contents)

@app.route('/compare', methods=['GET', 'POST'])
def compare():
    if request.method == 'GET':
        return render_template('data_comparison.html')

    prod_data = request.form['prod_data']
    int_data = request.form['int_data']
    results = compare_data.compare_tabular_inputs(prod_data, int_data)
    
    return render_template('data_comparison_results.html',
                           content=results)

@app.route('/compare_with_tolerance', methods=['GET', 'POST'])
def compare_with_tolerance():
    if request.method == 'GET':
        return render_template('data_comparison_results_with_tolerance.html')

    prod_data = request.form['prod_data']
    int_data = request.form['int_data']
    results = compare_data.compare_tabular_inputs_with_tolerance(prod_data,
                                                                 int_data)
    return render_template('data_comparison_results.html',
                           content=results)


if __name__ == "__main__":
    app.run(host='0.0.0.0',
            debug=True)
