import os
from flask import Flask
from .config import config_by_name

def create_app(config_name: str) -> Flask:
    app: Flask = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    return app

app: Flask = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')

from app import routes