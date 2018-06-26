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
        print(package_id)
        error = None

        res_path = os.getcwd() + '/thinClient_server/resources'

        error = 'OK'
        print('Send file ...')
        file = res_path+'/'+package_id
        return flask.send_file(file)

    # Bad Request
    return flask.make_response(
        flask.Response(error), 400)
