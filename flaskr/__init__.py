import os
import click
from flask import Flask
from . import (db, auth, pic)


def create_app(test_config=None):
    # create and configure the appgit add
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        FILEBASE=
         os.path.join(app.instance_path, 'pic_database')
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder/pic exists
    try:
        os.makedirs(app.config['FILEBASE'])
    except OSError:
        pass
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    #config for database
    db.init_app(app)


    #set up blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(pic.bp)
    app.add_url_rule('/', endpoint= 'index')
    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
