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

bp = Blueprint('list_packages', __name__, url_prefix='/list_packages')
client_table = 'thinClients'

@bp.route('/', methods=('GET', 'POST'))
def list_packages():
    if request.method == 'GET':
        db = get_db()
        cur = db.cursor()
        error = None

        res_path = os.getcwd() + '/thinClient_server/resources'
        packages = [f for f in os.listdir(res_path) if f.endswith('.zip')]

    if error is None:
        return jsonify(packages)

    # Bad Request
    return flask.make_response(
        flask.Response(error), 400)
