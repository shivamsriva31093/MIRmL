import logging

from flask import Flask
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

app = Flask(__name__)
mail = Mail()
moment = Moment()
db = SQLAlchemy(app)


def add_logger():
    file_handler = logging.FileHandler('app.log')
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)


def create_app(config_name):
    app.config.from_object(config[config_name])
    config[config_name].init_app(app=app)
    add_logger()
    mail.init_app(app)
    moment.init_app(app)

    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api_v1_0 import api as api_v1_0_blueprint
    app.register_blueprint(api_v1_0_blueprint, url_prefix='/api/v1.0')

    return app
