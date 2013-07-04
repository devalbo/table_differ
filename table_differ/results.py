
from flask import Blueprint, render_template, abort, request, url_for

blueprint = Blueprint('compare', __name__,
                      template_folder='templates')
