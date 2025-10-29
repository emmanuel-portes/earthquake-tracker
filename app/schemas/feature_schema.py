from marshmallow import Schema, fields

class FeatureSchema(Schema):
    feature_id = fields.Integer()
    feature_type = fields.Str()
    external_id = fields.Str()
    magnitude = fields.Float()
    event_date = fields.Date()
    url = fields.Str()
    tsunami = fields.Boolean()
    mag_type = fields.Str()
    title = fields.Str()
    longitude = fields.Float()
    latitude = fields.Float()
