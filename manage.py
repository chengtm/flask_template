#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Management script."""
import os

from flask import current_app
from flask import g, request
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server, Shell
from flask_script.commands import ShowUrls, Clean

from user.app import create_app
from user.settings import DevConfig, ProdConfig, LocalConfig
from user.extensions import db


my_env = os.environ.get('USER_TEMPLATE_ENV')
if my_env == 'prod':
    CONFIG = ProdConfig
elif my_env == 'dev':
    CONFIG = DevConfig
else:
    CONFIG = LocalConfig

HERE = os.path.abspath(os.path.dirname(__file__))
TEST_PATH = os.path.join(HERE, 'tests')

app = create_app(CONFIG)
manager = Manager(app)
migrate = Migrate(app, db)


def _make_context():
    """Return context dict for a shell session so you can access app, db, and the User model by default."""
    return {'app': app, 'db': db}


@app.before_request
def before_request():
    if current_app.config['DEBUG']:
        print(request.headers)


@app.after_request
def after_request(response):
    # cross domain setting
    response.headers.add('Access-Control-Allow-Origin', app.config['ACAO'])
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,If-Modified-Since')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('urls', ShowUrls())
manager.add_command('db', MigrateCommand)
manager.add_command('clean', Clean())

if __name__ == '__main__':
    manager.run()
