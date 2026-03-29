
from flask import Flask

from app.routes.features_route import feature
from app.exceptions.features_exception import error

from .database import database

from workers.celery_app import celery_init_app

from .config import config_by_name

def create_app(config_name: str = "prod") -> Flask:
    app: Flask = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    database.init_app(app)

    app.register_blueprint(feature)
    app.register_blueprint(error)

    celery_init_app(app)

    return app

