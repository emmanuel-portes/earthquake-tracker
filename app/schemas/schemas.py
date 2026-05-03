import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class PaginationSchema(BaseModel):
    current_page: int
    per_page: int
    total: int


class FeatureSchema(BaseModel):
    code: uuid.UUID
    usgs_class: str
    usgs_code: str
    magnitude: Decimal
    place: str
    event_date: datetime
    url: str
    tsunami: bool
    mag_type: str
    title: str
    longitude: Decimal
    latitude: Decimal


class SuccessfulResponse(BaseModel):
    successful: bool
    data: list[FeatureSchema] | list
    pagination: PaginationSchema
