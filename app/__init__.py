import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import config_by_name

database = SQLAlchemy()

def create_app(config_name: str) -> Flask:
    app: Flask = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    database.init_app(app)
    return app

app: Flask = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')

from app import routes, models