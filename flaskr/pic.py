from flask import (Blueprint, flash, g, session, redirect, render_template, request, url_for, current_app, send_from_directory)
from flaskr.auth import login_required
from werkzeug.exceptions import abort
import click
from flaskr.db import get_db
import os

bp= Blueprint('pic', __name__)

@bp.route('/')
def index():
    db = get_db()

    click.echo(type(db))
    return render_template('pic/index.html')


@bp.route('/upload', methods= ('GET', 'POST'))
def upload():
    if request.method == 'POST':
        file= request.files['img']


        error= None

        if file is None:

            error= 'attatch file'
            flash(error)
            redirect(url_for('pic.upload'))

        else:
            ext= file.filename.rsplit('.')[1]
            orig_name = file.filename

            db=get_db()

            last_id= db.execute('SELECT MAX(id) FROM pic').fetchone()[0]
            if not last_id:
                last_id= 0

            filename= str(last_id)+"."+ ext

            path= os.path.join(current_app.config['FILEBASE'], filename)

            file.save(path)

            db.execute('INSERT INTO pic (name, owner_id, string_path) VALUES (?,?,?)', (orig_name, g.user['id'], filename))
            db.commit()

            return redirect(url_for('index'))

    return render_template('pic/upload.html')

@bp.route('/view')
@login_required
def view():
    data = get_db()

    pictures= data.execute('SELECT name, string_path FROM pic WHERE owner_id= ? ORDER BY id DESC', (g.user['id'],)).fetchall()
    is_empty= not bool(pictures)

    return render_template('pic/view.html', pics=pictures, is_empty=is_empty)

@bp.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(current_app.config['FILEBASE'], filename, as_attachment=True)
