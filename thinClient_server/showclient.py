import functools
import datetime
import flask
from datetime import datetime, timedelta
import os, json
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from thinClient_server.db import get_db

bp = Blueprint('showclient', __name__, url_prefix='/showclient')
client_table = 'thinClients'

@bp.route('/', methods=('GET', 'POST'))
def show_client():
    if request.method == 'POST':
        client_id = str(request.form['client_id'])
        db = get_db()
        cur = db.cursor()
        error = None

        client_info = []
        if is_table_empty is not True:

            # check if client is alive
            cur.execute('SELECT id, latest_heartbeat FROM thinClients WHERE id=?', (client_id,))
            for row in cur.fetchall():
                dbtime = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
                timestamp = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.now())
                curtime = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                #print(str(dtime))
                if (dbtime + timedelta(seconds=30) < datetime.now()):
                    db.execute(
                    'UPDATE thinClients SET alive=? WHERE id=?'
                    , (0, client_id)
                    )
                    db.commit()
                else:
                    db.execute(
                    'UPDATE thinClients SET alive=? WHERE id=?'
                    , (1, client_id)
                    )
                    db.commit()

            # select information
            cur.execute('SELECT * FROM thinClients WHERE id=?', (client_id,))

            for client in cur.fetchall():
                for val in client:
                    client_info.append(val)

            return jsonify(client_info)

    # Bad Request
    return flask.make_response(
        flask.Response(error), 400)

# return true if table is empty
def is_table_empty(table):
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT COUNT(*) FROM {}'.format(table))
    if len(cur.fetchall()) > 0:
        return False
    return True
