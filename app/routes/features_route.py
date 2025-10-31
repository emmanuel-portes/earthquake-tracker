from flask import Blueprint, request

from app import database

from sqlalchemy.exc import NoResultFound

from marshmallow import ValidationError

from app.models.features_model import Feature
from app.models.comments_model import Comment

from app.schemas.feature_schema import FeatureSchema
from app.schemas.comment_schema import CommentSchema


feature = Blueprint('feature', __name__)

@feature.route("/", methods=['GET'])
def home():
    return {"message":"hello from earthquake-tracker"}, 200

@feature.route("/api/features", methods=["GET"])
def get_features():
    features: list[Feature] = Feature.query.all()
    response: dict = FeatureSchema(many=True).dump(features)
    return {"data": response}, 200

@feature.get("/api/features/<int:feature_id>")
def get_feature_by_id(feature_id: int):
    try:
        feature = Feature.query.filter(Feature.feature_id == feature_id).one()
    except NoResultFound:
        return {"message":"Feature could not be found"}, 404
    response: dict = FeatureSchema().dump(feature)
    return {"data": response}, 200

@feature.get('/api/features/<external_id>')
def get_feature_by_external_id(external_id: str):
    try:
        feature = Feature.query.filter(Feature.external_id == external_id).one()
    except NoResultFound:
        return {"message":"Feature could not be found"}, 404
    response: dict = FeatureSchema().dump(feature)
    return {"data": response}, 200

@feature.post('/api/features')
def insert_features_comments():

    unparsed_payload = request.get_json()

    if not unparsed_payload:
        return {'message':'No input data provided'}, 400
    
    try:
        payload: dict = CommentSchema().load(unparsed_payload)
    except ValidationError as error:
        return {'message': error.messages}, 422

    if (payload.get("commentary") is None) or (payload.get("feature_id") is None):
        return {'message': 'Comment or feature not availabe'}, 400
    
    feature_id: str = payload["feature_id"] 
    message: str = payload["commentary"]

    feature: Feature = Feature.query.filter(Feature.external_id == feature_id).first()

    if feature is None:
        return {'message':f'feature: {feature_id} is not registered'}, 400
    
    comment: Comment = Comment(commentary=message, feature_id=feature_id)

    database.session.add(comment)
    database.session.commit()

    response = CommentSchema().dump(Comment.query.get(comment.id))

    return {'message':'Comment succesfully added', "comment": response}, 201
