# -*- coding: utf-8 -*-

from flask import jsonify
from flask import current_app
from flask import g
from flask import request
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from sqlalchemy import or_

from .response import raise_401_response
from ..models.user import User


def unauthorized(message='unauthorized'):
    response = jsonify({'code': 401, 'message': message})
    response.status_code = 401
    return response


def forbidden(message='forbidden'):
    response = jsonify({'code': 403, 'message': message})
    response.status_code = 403
    return response


def get_user_from_auth_token(token, instance):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None
    except BadSignature:
        return None

    return instance.get_by_id(data['id'])


class UserSecurity(object):
    _model = User

    _share = False

    def _verify_password(self, mobile_or_token, password):
        if request.method == 'OPTIONS':
            token = request.values.get('token', False)
            if not token:
                return True

        token = request.values.get('token', None)
        if (not token) and mobile_or_token and (not password):
            token = mobile_or_token
        if token:
            user = get_user_from_auth_token(token, self._model)
            if user and user.active:
                g.current_user = user
                g.token_used = True
                return True

        if mobile_or_token and password:
            user = None
            if hasattr(self._model, 'mobile') and hasattr(self._model, 'email'):
                user = self._model.query.filter(or_(
                    self._model.mobile == str(mobile_or_token),
                    self._model.email == str(mobile_or_token))
                ).first()
            elif not hasattr(self._model, 'mobile') and hasattr(self._model, 'email'):
                user = self._model.query.filter(self._model.email == str(mobile_or_token)).first()

            if user and user.active and user.check_password(password):
                # set token
                user.generate_auth_token()
                g.current_user = user
                g.token_used = False
                return True

        if self._share:
            return True
        raise_401_response(message=u'用户名或者密码错误')

    def __init__(self, app=None, db=None):
        self.app = app
        self.db = db
        self.auth = HTTPBasicAuth()
        self.auth.error_handler(unauthorized)
        self.auth.verify_password(self._verify_password)

        if app is not None and db is not None:
            self.init_app(app, db)

    def init_app(self, app, db):
        if app is None:
            raise()

        self.app = app
        self.db = db


login_required = UserSecurity().auth.login_required
