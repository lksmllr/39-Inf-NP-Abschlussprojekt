import functools
import datetime
import flask
import datetime
import os, json
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from thinClient_server.db import get_db

bp = Blueprint('listclients', __name__, url_prefix='/listclients')
client_table = 'thinClients'

@bp.route('/', methods=('GET', 'POST'))
def list_clients():
    if request.method == 'GET':
        db = get_db()
        cur = db.cursor()
        error = None

        clients = []
        if is_table_empty is not True:
            cur.execute('SELECT id FROM thinClients')

            for client in cur.fetchall():
                clients.append(str(client[0]))

        return jsonify(clients)

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
