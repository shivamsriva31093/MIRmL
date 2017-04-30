from flask import jsonify

from . import api


@api.route('/test/<name>/', methods=['GET'])
def met(name):
    return jsonify({'user': name})
