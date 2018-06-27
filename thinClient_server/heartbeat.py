import functools
import datetime
import flask
import datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from thinClient_server.db import get_db

bp = Blueprint('heartbeat', __name__, url_prefix='/heartbeat')
client_table = 'thinClients'

@bp.route('/', methods=('GET', 'POST'))
def latest_heartbeat():
    if request.method == 'POST':
        thinClient_id = request.form['id']
        thinClient_cpu = request.form['cpu']
        thinClient_ram = request.form['ram']
        thinClient_gpu = request.form['gpu']
        #thinClient_id = request.form.get('id')
        db = get_db()
        cur = db.cursor()
        error = None
        if not thinClient_id:
            error = 'thinClient_id is required.'
        # If client exists update timestamp
        elif db.execute(
            'SELECT latest_heartbeat FROM thinClients WHERE id = ?', (thinClient_id,)
        ).fetchone() is not None:
            timestamp = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
            db.execute(
            'UPDATE thinClients SET latest_heartbeat=? WHERE id=?'
            , (timestamp, thinClient_id)
            )
            db.commit()
            error = 'ThinClient {} is already registered.'.format(thinClient_id)
        # if new client register in db
        if error is None:
            timestamp = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
            db.execute(
                'INSERT INTO thinClients (id, latest_heartbeat, cpu, ram_in_gb, gpu) VALUES (?,?,?,?,?)',
                (thinClient_id, timestamp, thinClient_cpu, thinClient_ram, thinClient_gpu)
            )
            # print('Registered Client with id: '+thinClient_id)
            db.commit()
            # OK
            #print_table(client_table)
            return flask.make_response(
                flask.Response('OK'), 200)
        flash(error)
        #print_table(client_table)
        return flask.make_response(
            flask.Response('OK'), 200)
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

# return size of table
def table_size(table):
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT COUNT(*) FROM {}'.format(table))
    print('table size: '+str(len(cur.fetchall())))

# print table
def print_table(table):
    print('\n --- REGISTERED THIN CLIENTS ARE: ---\n')
    if is_table_empty(client_table) is not True:
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM thinClients")
        for row in cur.fetchall():
            client = []
            for val in row:
                client.append(str(val))
            print(client)
    else:
        print('Empty Table: '+client_table)
    print('\n --- END OF TABLE ---\n')
