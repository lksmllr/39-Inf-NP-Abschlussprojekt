import functools
import datetime
import flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from thinClient_server.db import get_db


bp = Blueprint('heartbeat', __name__, url_prefix='/heartbeat')

@bp.route('/', methods=('GET', 'POST'))
def latest_heartbeat():
    if request.method == 'POST':
        thinClient_id = request.form['id']
        #thinClient_id = request.form.get('id')
        print(thinClient_id)
        db = get_db()
        error = None

        if not thinClient_id:
            error = 'thinClient_id is required.'

        elif db.execute(
            'SELECT latest_heartbeat FROM thinClients WHERE id = ?', (thinClient_id,)
        ).fetchone() is not None:
            error = 'ThinClient {} is already registered.'.format(thinClient_id)

        if error is None:
            db.execute(
                'INSERT INTO thinClients (thinClient_id,latest_heartbeat) VALUES (?,?)',
                (thinClient_id, datetime.datetime.now()).split('.')[0]
            )
            db.commit()
            return flask.make_response(
                flask.Response('OK'), 200)

        flash(error)

    return flask.make_response(
                flask.Response(error), 400)
