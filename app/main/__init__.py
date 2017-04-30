from flask import Blueprint

main = Blueprint('main', __name__)

from .views import views
from . import errors
