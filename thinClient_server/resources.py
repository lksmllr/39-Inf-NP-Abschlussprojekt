import functools
import datetime
import flask
import datetime
import os
from flask import (
    Blueprint, flash, g, redirect, render_template
    , request, session, url_for, send_file
)


bp = Blueprint('resources', __name__, url_prefix='/resources')

@bp.route('/', methods=('GET', 'POST'))
def send_file():
    if request.method == 'POST':
        package_id = request.form['package_id']
        error = None
        res_path = os.getcwd() + '/thinClient_server/resources'
        file = res_path+'/'+package_id
        try:
            return flask.send_file(file)
        except FileNotFoundError:
            error = 'ohje'
        if error is not None:
            # File not found
            return flask.make_response(
                flask.Response(error), 404)

    # Bad Request
    return flask.make_response(
        flask.Response(error), 400)
