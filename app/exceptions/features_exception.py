from flask import Blueprint, jsonify, make_response
from . import AppException

error: Blueprint = Blueprint('errors', __name__)

@error.app_errorhandler(AppException)
def handle_custom_exception(err):
    return make_response(
        jsonify(err.to_dict()), 
        err.status_code
    )