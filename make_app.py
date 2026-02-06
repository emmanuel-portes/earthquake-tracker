import os
from flask import Flask

from celery import Celery

from app import create_app

flask_app: Flask = create_app(os.getenv('APP_ENV') or 'dev')
celery_app: Celery = flask_app.extensions['celery']

