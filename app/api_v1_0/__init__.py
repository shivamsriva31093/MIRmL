from flask import Blueprint

api = Blueprint('api', __name__)

# add any dependent modules of the api here to prevent any circular dependencies

from . import test
from . import predict
from . import errors