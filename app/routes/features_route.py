from flask import Blueprint, request

from http import HTTPStatus

from app.constants import Constants
from app.services.features_service import FeatureService
from app.exceptions import DataNotProvidedException, InvalidValueException

feature_service: FeatureService = FeatureService()
feature = Blueprint('feature', __name__)

@feature.route("/", methods=['GET'])
def home():
    return {"message":"hello from earthquake-tracker"}, HTTPStatus.OK

@feature.get("/api/features")
def get_features():
    page: int = request.args.get("page", 1, type=int)
    number_of_items: int = request.args.get("no_items", 10, type=int)
    mag_type: str = request.args.get("mag_type", None, type=str)

    if mag_type is not None and mag_type not in Constants.MAG_TYPES:
        message: str = f"Cannot filter by mag type: {mag_type}"
        raise InvalidValueException(message=message)

    if number_of_items > Constants.PER_PAGE_LIMIT:
        message: str = f"The limit for number of items is exceded: {number_of_items}"
        raise InvalidValueException(message=message)

    response: dict = feature_service.get_features(page, number_of_items, mag_type)
    return {
        "status": HTTPStatus.OK, 
        "data": response.get("data", list()),
        "pagination": response.get("pagination", dict())
    }, HTTPStatus.OK

@feature.get("/api/features/<int:feature_id>")
def get_feature_by_id(feature_id: int):
    response: dict = feature_service.get_feature_by_id(feature_id)
    return {
        "status": HTTPStatus.OK, 
        "data": response
    }, HTTPStatus.OK

@feature.get('/api/features/<external_id>')
def get_feature_by_external_id(external_id: str):
    response: dict = feature_service.get_feature_by_external_id(external_id)
    return {
        "status": HTTPStatus.OK, 
        "data": response
    }, HTTPStatus.OK

@feature.post('/api/features')
def insert_features_comments():
    data: dict = request.get_json()
    if not data:
        raise DataNotProvidedException("data not found in payload")
    
    response: dict = feature_service.save_feature_comment(data)
    return {
        "status":HTTPStatus.CREATED, 
        'message':'Comment succesfully added', "data": response
    }, HTTPStatus.CREATED
