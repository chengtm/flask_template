# -*- coding: utf-8 -*-
import datetime as dt

from flask import g, current_app
from flask import request

from .response import success_response, RestfulBase
from .security import login_required


class UserLogin(RestfulBase):
    @login_required
    def post(self):
        last_login_ip = request.remote_addr
        login_count = (g.current_user.login_count + 1) if g.current_user.login_count else 1
        g.current_user.update(last_login_time=dt.datetime.now(),
                              login_count=login_count,
                              last_login_ip=last_login_ip)

        base_info = {
            'id': g.current_user.id,
            'name': g.current_user.name,
            'mobile': g.current_user.mobile,
            'email': g.current_user.email,
            'token': g.current_user.generate_auth_token(expiration=current_app.config['TOKEN_EXPIRATION_TIME'])
        }
        return success_response(data=base_info)
