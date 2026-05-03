import uuid
from datetime import datetime
from decimal import Decimal

from sqlmodel import Field, SQLModel, UniqueConstraint


class FeatureBase(SQLModel):
    usgs_class: str = Field(max_length=8)
    usgs_code: str = Field(max_length=15)
    magnitude: Decimal = Field(max_digits=4, decimal_places=2)
    place: str = Field(max_length=100)
    event_date: datetime
    url: str = Field(max_length=75)
    tsunami: bool
    mag_type: str = Field(max_digits=3)
    title: str = Field(max_length=100)
    longitude: Decimal = Field(max_digits=15, decimal_places=7)
    latitude: Decimal = Field(max_digits=15, decimal_places=7)

    __table_args__ = UniqueConstraint("usgs_code")

    def __repr__(self) -> str:
        return f"Feature({self.usgs_code} - {self.usgs_class})"


class Feature(FeatureBase, table=True):
    code: uuid.UUID = Field(default=None, primary_key=True)

    def __repr__(self) -> str:
        return f"Feature({self.usgs_code} - {self.code})"
