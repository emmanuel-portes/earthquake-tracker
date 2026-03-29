from datetime import date, datetime, timedelta

from flask import Blueprint, request

from http import HTTPStatus

from celery.result import AsyncResult

from app.constants import Constants
from app.services.features_service import FeatureService
from app.exceptions import DataNotProvidedException, InvalidValueException

from workers.task import ingest_into_database, test_task_queue

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

@feature.get("/api/features/<int:feature_code>")
def get_feature_by_code(feature_code: int):
    response: dict = feature_service.get_feature_by_code(feature_code)
    return {
        "status": HTTPStatus.OK, 
        "data": response
    }, HTTPStatus.OK

@feature.get('/api/features/<usgs_code>')
def get_feature_by_usgs_code(usgs_code: str):
    response: dict = feature_service.get_feature_by_usgs_code(usgs_code)
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

@feature.post("/api/features/ingest")
def ingest_features() -> dict[str, object]:
    starttime: date = request.args.get('starttime', None, date)
    endtime: date = request.args.get('endtime', None, date)

    if not starttime:
        starttime = (datetime.now() - timedelta(days=1)).date()
    if not endtime:
        endtime: date = datetime.now().date()

    url: str = f'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={starttime}&endtime={endtime}'
    result = ingest_into_database.delay(url)
    return {
        "status": HTTPStatus.CREATED,
        "id": result.id
    }, HTTPStatus.CREATED

@feature.get("/api/features/ingest/<task_id>")
def get_task_result(task_id: str) -> dict[str, object]:
    result = AsyncResult(task_id)
    return {
        "status": HTTPStatus.OK,
        "ready": result.ready(),
        "successful": result.successful(),
        "value": result.result if result.ready() else None
    }, HTTPStatus.OK