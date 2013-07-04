
from flask import Blueprint, render_template, abort, request, url_for

blueprint = Blueprint('baseline', __name__,
                      template_folder='templates')
