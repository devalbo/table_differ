import compare_data
import cPickle as pickle
import uuid, os
import td_config
import reverseproxied

from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
import flask

app = Flask(__name__)
app.wsgi_app = reverseproxied.ReverseProxied(app.wsgi_app)


def convert_data_to_table(table_data):
    grid_data = table_data['grid_data']
    row_count = int(table_data['row_count'])
    col_count = int(table_data['col_count'])
    td = [[grid_data[i + (j * col_count)]
           for i in range(col_count)]
          for j in range(row_count)]

    table_info = {}
    table_info["row_count"] = row_count
    table_info["col_count"] = col_count

    return table_info, td

@app.route('/')
def index():
    return tables_input()

@app.route('/tables_input', methods=['GET', 'POST'])
def tables_input():
    if request.method == 'GET':
        return render_template('tables_input.html')

    table1 = request.json['dataTable1']
    table2 = request.json['dataTable2']
    t1_info, table1 = convert_data_to_table(table1)
    t2_info, table2 = convert_data_to_table(table2)
    diffs, sames = compare_data.compare_tables(table1, table2, None)
    results = {"t1_info": t1_info,
               "t2_info": t2_info,
               "diffs": diffs,
               "sames": sames}
    results_id = uuid.uuid4()
    pickle.dump(results, open(os.path.join("compare_results",
                                           "%s.p" % results_id),
                              "wb"))
    redirect_url = url_for('show_results', results_id=results_id)
    return flask.jsonify(redirect_url=redirect_url)

@app.route('/results/<results_id>', methods=['GET'])
def show_results(results_id):
    options = td_config.RenderTableOptions()
    results = pickle.load(open(os.path.join("compare_results",
                                            "%s.p" % results_id),
                               "rb"))
    t1_row_count = results["t1_info"]["row_count"]
    t2_row_count = results["t2_info"]["row_count"]
    if t1_row_count != t2_row_count:
        return "Error - different numbers of rows (%s / %s)" % (t1_row_count,
                                                                t2_row_count)

    t1_col_count = results["t1_info"]["col_count"]
    t2_col_count = results["t2_info"]["col_count"]
    if t1_col_count != t2_col_count:
        return "Error - different numbers of columns (%s / %s)" % (t1_col_count,

                                                                   t2_col_count)
    
    table_rows = []
    for row_index in range(t1_row_count):
        table_row = []
        for col_index in range(t1_col_count):
            if (row_index, col_index) in results["sames"]:
                item = ("%s" % results["sames"][(row_index, col_index)], "ok")
            else:
                item = ("Expected: %s --- Actual: %s" %
                        results["diffs"][(row_index, col_index)],
                        "mismatch")
                        
            table_row.append(item)

        table_rows.append(table_row)

    return render_template('data_comparison_results_handson.html',
                           table_rows=table_rows,
                           options=options)


if __name__ == "__main__":
    app.run(host='0.0.0.0',
            debug=True)
