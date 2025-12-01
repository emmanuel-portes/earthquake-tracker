from flask import Blueprint, request

from http import HTTPStatus

from app.services.features_service import FeatureService

from app.exceptions import DataNotProvidedException

feature_service: FeatureService = FeatureService()

feature = Blueprint('feature', __name__)

@feature.route("/", methods=['GET'])
def home():
    return {"message":"hello from earthquake-tracker"}, HTTPStatus.OK

@feature.get("/api/features")
def get_features():
    page: int = request.args.get("page")
    number_of_items: int = request.args.get("no_items")
    response: list = feature_service.get_features(page, number_of_items)
    return {
        "status": HTTPStatus.OK, 
        "data": response
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
