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
        cur = db.cursor()
        error = None

        if not thinClient_id:
            error = 'thinClient_id is required.'

        elif db.execute(
            'SELECT latest_heartbeat FROM thinClients WHERE id = ?', (thinClient_id,)
        ).fetchone() is not None:
            db.execute(
            'UPDATE thinClients SET latest_heartbeat=? WHERE id=?', ("time", thinClient_id)
            )
            cur.execute("SELECT * FROM thinClients")
            for row in cur.fetchall():
                for val in row:
                    print(str(val))
            print("Client "+thinClient_id)
            error = 'ThinClient {} is already registered.'.format(thinClient_id)

        if error is None:
            db.execute(
                'INSERT INTO thinClients (id,latest_heartbeat) VALUES (?,?)',
                (thinClient_id, "time")
            )
            print('Registered Client with id: '+thinClient_id)
            db.commit()
            return flask.make_response(
                flask.Response('OK'), 200)

        flash(error)
        print(error)

    return flask.make_response(
                flask.Response(error), 400)
