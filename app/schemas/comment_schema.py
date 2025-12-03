from marshmallow import Schema, fields

class CommentSchema(Schema):
    id = fields.Integer(dump_only=True)
    comment = fields.String(data_key="comment")
    usgs_code = fields.String()