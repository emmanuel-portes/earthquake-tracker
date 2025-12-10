from datetime import datetime, date
from app.constants import Constants
from marshmallow import Schema, fields, pre_load, validate, ValidationError

def validate_string_field(string: str) -> None:
    if string is None:
        raise ValidationError("field must not be empty.")
    
    if len(string) <= 0:
        raise ValidationError("field's length shouldn't be below or equal Zero.")


class CoordinatesSchema(Schema):
    longitude = fields.Float()
    latitude = fields.Float()

class LinkSchema(Schema):
    url = fields.Str()

class AttributesSchema(Schema):
    usgs_code = fields.Str()
    magnitude = fields.Float()
    event_date = fields.Date(data_key="date")
    place = fields.Str()
    tsunami = fields.Boolean()
    mag_type = fields.Str()
    title = fields.Str()

class FeatureSchema(Schema):
    code = fields.Integer(data_key="id")
    usgs_class = fields.Str(data_key="type")
    attributes = fields.Method("get_attributes")
    coordinates = fields.Method("get_coordinates")
    links = fields.Method("get_links")

    def get_attributes(self, obj) -> dict:
        return AttributesSchema().dump(obj)
    
    def get_coordinates(self, obj) -> dict:
        return CoordinatesSchema().dump(obj)
    
    def get_links(self, obj) -> dict:
        return LinkSchema().dump(obj)

class USGSFeatureSchema(Schema):
    usgs_class = fields.Str(data_key="type")
    usgs_code = fields.Str(data_key="id")
    place = fields.Str(validate=validate_string_field)
    event_date = fields.Method(data_key="time", deserialize="time_format")
    url = fields.Str(validate=validate.URL(relative=False, absolute=True))
    tsunami = fields.Boolean()
    mag_type = fields.Str(data_key="magType", validate=validate.OneOf(Constants.MAG_TYPES))
    title = fields.Str(validate=validate_string_field)
    magnitude = fields.Float(data_key='mag', validate=validate.Range(min=Constants.MIN_MAGNITUDE, max=Constants.MAX_MAGNITUDE))
    latitude = fields.Float(validate=validate.Range(min=Constants.MIN_LATITUDE, max=Constants.MAX_LATITUDE))
    longitude = fields.Float(validate=validate.Range(min=Constants.MIN_LONGITUDE, max=Constants.MAX_LONGITUDE))

    def time_format(self, timestamp:int) -> date:
        timestamp = timestamp / 1000
        return datetime.fromtimestamp(timestamp).date()

    @pre_load
    def process_incomming_data(self, data, **kwargs) -> dict:
        return {
            "type": data["type"],
            "id": data["id"],
            "mag": data["properties"]["mag"],
            "place": data["properties"]["place"],
            "time": data["properties"]["time"],
            "url": data["properties"]["url"],
            "tsunami": data["properties"]["tsunami"],
            "magType": data["properties"]["magType"],
            "title": data["properties"]["title"],
            "longitude": data["geometry"]["coordinates"][0],
            "latitude": data["geometry"]["coordinates"][1],
        }



