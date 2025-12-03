import os

from http import HTTPStatus

from flask import Blueprint, jsonify, make_response, request

from werkzeug.exceptions import HTTPException, NotFound

from . import AppException

from sqlalchemy.exc import SQLAlchemyError

from marshmallow import ValidationError

error: Blueprint = Blueprint('errors', __name__)

@error.app_errorhandler(AppException)
def handle_custom_exception(error):
    return make_response(
        jsonify(error.to_dict()), error.status_code
    )

@error.app_errorhandler(SQLAlchemyError)
def handle_orm_exception(error):
    platform: str = os.getenv('BOILERPLATE_ENV', "dev")
    if platform != "prod":
        return make_response(
            jsonify({
                "message": error.message, 
                "status": HTTPStatus.INTERNAL_SERVER_ERROR
            }),
            HTTPStatus.INTERNAL_SERVER_ERROR
        )

    return make_response(
        jsonify({
            "message":"Something went wrong. Contact the Administrator", 
            "status": HTTPStatus.INTERNAL_SERVER_ERROR 
        }),
        HTTPStatus.INTERNAL_SERVER_ERROR
    )

@error.app_errorhandler(ValueError)
@error.app_errorhandler(ValidationError)
def handle_validation_error(error):
    platform: str = os.getenv('BOILERPLATE_ENV')
    if platform != "prod":
        return make_response(
            jsonify({
                "message": error.message, 
                "status": HTTPStatus.UNPROCESSABLE_ENTITY 
            }),
            HTTPStatus.UNPROCESSABLE_ENTITY
        )

    return make_response(
        jsonify({
            "message":"Something while validating the fields", 
            "status": HTTPStatus.UNPROCESSABLE_ENTITY 
        }),
        HTTPStatus.UNPROCESSABLE_ENTITY
    )

@error.app_errorhandler(NotFound)
def handle_not_found_exception(error):
    source: str = request.remote_addr
    path: str = request.url

    return make_response(
        jsonify({
            "message": f"Client: {source} requested not available url: {path}",
            "status": HTTPStatus.NOT_FOUND
        }),
        HTTPStatus.NOT_FOUND
    )

@error.app_errorhandler(HTTPException)
def handle_base_http_exception(error):
    return make_response(
        jsonify({
            "message": error.description,
            "status": error.code
        }), error.code
    )   

@error.app_errorhandler(Exception)
def handle_base_exception(error):
    platform: str = os.getenv('BOILERPLATE_ENV', "dev")

    if platform != "prod":
        return make_response(
            jsonify({
                "name":error.__class__.__name__,
                "message": error.args[0],
                "status": HTTPStatus.INTERNAL_SERVER_ERROR
            }), HTTPStatus.INTERNAL_SERVER_ERROR
        )
    
    return make_response(
    jsonify({
        "message":"Something went wrong. Contact the Administrator", 
        "status": HTTPStatus.INTERNAL_SERVER_ERROR 
    }),
    HTTPStatus.INTERNAL_SERVER_ERROR
)
    
    