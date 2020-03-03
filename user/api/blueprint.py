# -*- coding: utf-8 -*-
from flask import Blueprint
from flask_restful import Api

from ..extensions import csrf_protect
from .login import UserLogin

user_blueprint = Blueprint('user', __name__, url_prefix='/')

user_api = Api(user_blueprint, prefix='user', decorators=[csrf_protect.exempt])
user_api.add_resource(UserLogin, '/login')

