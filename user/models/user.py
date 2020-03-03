# -*- coding: utf-8 -*-


from .base import *
from .mixin import PasswordUserMixin


class User(PasswordUserMixin, SurrogatePK, Model):

    __tablename__ = 'user'

    mobile = Column(db.String(30), unique=True, index=True, nullable=False)
    email = Column(db.String(80), unique=True, index=True, nullable=False, default='')
    name = Column(db.String(50), nullable=False, default='')
    city = Column(db.String(128), nullable=False, default='')
    qq = Column(db.String(20), nullable=False, default='')

    login_count = Column(db.Integer, nullable=False, default=0)
    last_login_time = Column(db.DateTime, nullable=False, default=dt.datetime.now)
    last_login_ip = Column(db.String(30), nullable=False, default='')

    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.now)
    updated_at = Column(db.DateTime, nullable=False, default=dt.datetime.now)

    active = Column(db.Boolean(), default=True)
    memo = Column(db.String(255), nullable=False, default='')

