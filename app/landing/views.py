from . import blueprint

from flask import render_template, url_for


@blueprint.route('/')
@blueprint.route('/index')
def index():
    return render_template('index.html')
