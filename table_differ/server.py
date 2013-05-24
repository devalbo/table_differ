import compare_data
import cPickle as pickle
import uuid, os
import td_config
import td_parsers
import reverseproxied

from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from flask import Markup
import flask
from werkzeug import secure_filename


app = Flask(__name__)
app.wsgi_app = reverseproxied.ReverseProxied(app.wsgi_app)


@app.route('/')
def index():
    return tables_input()

@app.route('/tables_input', methods=['GET', 'POST'])
def tables_input():
    if request.method == 'GET':
        return render_template('tables_input.html')

    t1_info, table1 = td_parsers.load_table_from_handson_json(request.json['dataTable1'])
    t2_info, table2 = td_parsers.load_table_from_handson_json(request.json['dataTable2'])
    diffs, sames = compare_data.compare_td_tables(table1, table2, None)
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
                item = (Markup("Expected: %s<br>Actual: %s" %
                               results["diffs"][(row_index, col_index)]),
                        "mismatch")

            table_row.append(item)

        table_rows.append(table_row)

    return render_template('data_comparison_results_handson.html',
                           table_rows=table_rows,
                           options=options)


UPLOAD_FOLDER = 'C:\\uploaded_files'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'xls', 'csv'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

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

from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if __name__ == "__main__":
    app.run(host='0.0.0.0',
            debug=True)
