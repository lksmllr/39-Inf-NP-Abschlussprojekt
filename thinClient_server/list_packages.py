import functools
import datetime
import flask
import datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
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
        
