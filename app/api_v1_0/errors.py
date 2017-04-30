from flask import jsonify
from flask import request, app

from . import api


def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response


class InvalidURLParameters(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@api.errorhandler(InvalidURLParameters)
def handle_invalid_url_parameter(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@api.app_errorhandler(404)
def handle_not_found(e):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp
