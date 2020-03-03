# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from .extensions import (
    bcrypt,
    csrf_protect,
    db,
)


def create_app(config_object):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    bcrypt.init_app(app)
    csrf_protect.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    from .api import user_blueprint
    app.register_blueprint(user_blueprint)
    return None
