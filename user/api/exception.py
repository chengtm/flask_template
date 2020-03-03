# -*- coding: utf-8 -*-


class ApiException(BaseException):
    http_status_code = 200

    def __init__(self, code, message=None, data=None):
        self.code = code
        self.message = message
        self.data = data

    def __str__(self):
        return {
            'code': self.code,
            'message': self.message,
            'data': self.data,
        }
    

class BadRequestException(ApiException):
    http_status_code = 400

    def __init__(self, code=400, message=None, data=None):
        super(BadRequestException, self).__init__(code, message, data)


class UnauthorizedException(ApiException):
    http_status_code = 401

    def __init__(self, code=401, message=None, data=None):
        super(UnauthorizedException, self).__init__(code, message, data)


class ForbiddenException(ApiException):
    http_status_code = 403

    def __init__(self, code=403, message=None, data=None):
        super(ForbiddenException, self).__init__(code, message, data)


class NotFoundException(ApiException):
    http_status_code = 404

    def __init__(self, code=404, message=None, data=None):
        super(NotFoundException, self).__init__(code, message, data)


ServiceException = ApiException
