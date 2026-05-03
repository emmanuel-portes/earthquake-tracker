from fastapi import APIRouter, Depends, status

from app.core.constants import MAG_TYPES, PER_PAGE_LIMIT
from app.database.session import get_session
from app.schemas.schemas import SuccessfulResponse

# from app.exceptions import InvalidValueException
from app.services.service import Service

router: APIRouter = APIRouter(prefix="/features")


@router.get("/", status_code=status.HTTP_200_OK)
def get_features(
    page: int = 1,
    number_of_features: int = 10,
    mag_type: str | None = None,
    service: Service = Depends(get_session),
) -> SuccessfulResponse:
    if mag_type and mag_type not in MAG_TYPES:
        message: str = f"Cannot filter by mag type: {mag_type}"
        # raise InvalidValueException(message=message)

    if number_of_features > PER_PAGE_LIMIT:
        message = f"The limit for number of items is exceded: {number_of_features}"
        print(message)
        # raise InvalidValueException(message=message)

    successful, data, pagination = service.get_features(
        page, number_of_features, mag_type
    ).values()

    return SuccessfulResponse(successful=successful, data=data, pagination=pagination)


"""
@router.get("/<int:feature_code>")
def get_feature_by_code(feature_code: int):
    response: dict = feature_service.get_feature_by_code(feature_code)
    return {"status": HTTPStatus.OK, "data": response}, HTTPStatus.OK


@router.get("/<usgs_code>")
def get_feature_by_usgs_code(usgs_code: str):
    response: dict = feature_service.get_feature_by_usgs_code(usgs_code)
    return {"status": HTTPStatus.OK, "data": response}, HTTPStatus.OK


@router.post("/")
def insert_features_comments():
    data: dict = request.get_json()
    if not data:
        raise DataNotProvidedException("data not found in payload")

    response: dict = feature_service.save_feature_comment(data)
    return {
        "status": HTTPStatus.CREATED,
        "message": "Comment succesfully added",
        "data": response,
    }, HTTPStatus.CREATED


 @router.post("/ingest")
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

@router.get("ingest/<task_id>")
def get_task_result(task_id: str) -> dict[str, object]:
    result = AsyncResult(task_id)
    return {
        "status": HTTPStatus.OK,
        "ready": result.ready(),
        "successful": result.successful(),
        "value": result.result if result.ready() else None
    }, HTTPStatus.OK """
