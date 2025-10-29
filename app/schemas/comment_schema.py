from marshmallow import Schema, fields

class CommentSchema(Schema):
    id = fields.Integer(dump_only=True)
    commentary = fields.String(data_key="comment")
    feature_id = fields.String()