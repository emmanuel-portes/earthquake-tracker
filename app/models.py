from dataclasses import dataclass
from datetime import date

@dataclass
class Feature:
    id: int
    type: str
    external_id: str
    magnitude: float
    place: str
    event_date: date
    url: str
    tsunami: bool
    mag_type: str
    title: str
    longitude: float
    latitude: float

@dataclass
class Comment:
    id: int
    commentary: str
    feature_id: str