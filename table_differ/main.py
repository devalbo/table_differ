
from flask import url_for
from flask import redirect

from admin import admin
from api import api
from app import app
from table_differ.blueprints import baselines, compare, downloads, results

app.register_blueprint(compare.blueprint, url_prefix='/compare')
app.register_blueprint(baselines.blueprint, url_prefix='/baselines')
app.register_blueprint(results.blueprint, url_prefix='/results')
app.register_blueprint(downloads.blueprint, url_prefix='/downloads')

@app.route('/')
def index():
    return redirect(url_for('compare.copy_paste_compare'))


admin.setup()
api.setup()

if __name__ == "__main__":
    app.run(host='0.0.0.0',
            port=5005,
            debug=True)