# -*- coding: utf-8 -*-
from flask_restful import Resource
from werkzeug.exceptions import HTTPException

from .exception import \
    ApiException, NotFoundException, BadRequestException, \
    UnauthorizedException, ForbiddenException


class RestfulBase(Resource):
    _model_service = None

    def pre_request(f):
        def method(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except ApiException as ex:
                return ex.__str__(), ex.http_status_code
            except HTTPException as ex:
                return ex.get_response()
        return method
    method_decorators = [pre_request]

    def get_context_data(self, *fields, **arguments):
        return {k: v for k, v in arguments.items() if k in fields}

    def filter_valid_args(self, **args):
        for k, v in args.items():
            if v is not None:
                continue
            args.pop(k)


def raise_error_response(error_code, message='error', data=None):
    raise ApiException(error_code, message, data)


def raise_400_response(code=400, message=u'请求参数错误', data=None):
    raise BadRequestException(code=code, message=message, data=data)


def raise_401_response(code=401, message=u'请求未授权', data=None):
    raise UnauthorizedException(code=code, message=message, data=data)


def raise_403_response(code=403, message=u'请求被拒绝', data=None):
    raise ForbiddenException(code=code, message=message, data=data)


def raise_404_response(code=404, message=u'未找到', data=None):
    raise NotFoundException(code=code, message=message, data=data)


def success_response(message='success', data=None):
    result = {
        'code': 0,
        'message': message
    }
    if data is not None:
        result['data'] = data

    return result, 200
