import functools
import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('heartbeat', __name__, url_prefix='/heartbeat')

@bp.route('/heartbeat', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        thinClient_id = request.form['id']
        db = get_db()
        error = None

        if not thinClient_id:
            error = 'thinClient_id is required.'

        elif db.execute(
            'SELECT id FROM thinClients WHERE id = ?', (thinClient_id,)
        ).fetchone() is not None:
            error = 'ThinClient {} is already registered.'.format(thinClient_id)

        if error is None:
            db.execute(
                'INSERT INTO thinClients (thinClient_id,latest_heartbeat) VALUES (?,?)',
                (thinClient_id, datetime.datetime.now()).split('.')[0])
            )
            db.commit()
