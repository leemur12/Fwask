import functools
import datetime
from flask import( Blueprint, flash, g, redirect, render_template, request, session)
from werkzeug.sercurity import check_password_hash, generate_password
from flaskr.db import get_db

bp=Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username= request.form['username']
        password= request.form['password']
        date= datetime.datetime.today()
        db= get_db()

        error = None

        if not username.strip():
            error = 'Username is required.'

        elif not password.strip():
            error = 'Password is required'

        elif db.execute('SELECT id FROM user WHERE username =?', (username)).fetchone() is not None:
            error= 'User {} is already registered'.format(username)

        if error is None:
            db.execute('INSERT INTO user (username, password, date_joined) VALUES(?,?,?)'),
            (username, generate_password_hash(password), date)
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/reigister.html')

@bp.route('/login', methods= ('GET', 'POST'))

def login():

    if request.method()= 'POST':
        username= request.form['username']
        password= request.form['password']

        db= get_db()
        error=None

        user= db.execute('SELECT id FROM user WHERE username=?', (username)).fetchone()
