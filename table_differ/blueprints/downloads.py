
import pickle, StringIO
# import jsonpickle, StringIO
from flask import Blueprint, render_template, abort, request, url_for, Markup, send_file, jsonify
import td_config, td_comparison
from app import app
import models

blueprint = Blueprint('downloads', __name__,
                      template_folder='templates')

@blueprint.route('/comparisons/<int:comparison_id>/tables/actual')
def downloads_actual_table(comparison_id):
    img = models.ComparisonResult.get(models.ComparisonResult.id == comparison_id).pickled_actual_table

    strIO = StringIO.StringIO()
    strIO.write(img)
    strIO.seek(0)
    return send_file(strIO,
                     attachment_filename="comparison-overview-%s.png" % comparison_id,
                     as_attachment=True)


