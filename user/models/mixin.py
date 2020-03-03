# -*- coding: utf-8 -*-

from flask import current_app
from flask.ext.login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from .base import Column, db
from ..extensions import bcrypt


class ReprMixin(object):
    def __repr__(self):
        return u'<{0}: {1}>'.format(self.__class__.name, self.name).encode('utf-8')


class PasswordUserMixin(UserMixin):
    #: The hashed password
    password = Column(db.String(128), nullable=True)

    def set_password(self, password, commit=True):
        self.password = bcrypt.generate_password_hash(password)
        if commit:
            self.save()

    def check_password(self, value):
        return bcrypt.check_password_hash(self.password, value)

    def generate_auth_token(self, expiration=3600 * 24 * 7):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.id}).decode('ascii')

    @property
    def name(self):
        return self.name or self.username or "无名氏"

    @property
    def classname(self):
        return self.__class__.__name__


AnonymousUserMixin = AnonymousUserMixin
