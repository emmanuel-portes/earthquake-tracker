from app import database

from app.models.features_model import Feature
from app.models.comments_model import Comment

from app.schemas.feature_schema import FeatureSchema
from app.schemas.comment_schema import CommentSchema

from app.exceptions import FeatureNotFoundException

class FeatureService:

    def get_features(self, page:int = 1, number_of_items:int = 10) -> list[dict]:
        data: list[Feature] = Feature.query.order_by(Feature.event_date.desc()).paginate(page=page, per_page=number_of_items)
        features:list[FeatureSchema] = FeatureSchema(many=True).dump(data.items)
        return features
    
    def get_feature_by_id(self, id: int) -> dict:
        data: Feature | None = Feature.query.filter(Feature.feature_id == id).first()
        if data is None:
            raise FeatureNotFoundException(f"Feature of ID: {id} was not found")
        feature: FeatureSchema = FeatureSchema().dump(data)
        return feature
        
    def get_feature_by_external_id(self, id: str) -> dict:
        data: Feature | None = Feature.query.filter(Feature.external_id == id).first()
        if data is None:
            raise FeatureNotFoundException(f"Feature of external ID: {id} was not found")
        feature: dict = FeatureSchema().dump(data)
        return feature

    def save_feature_comment(data:dict[str,str]) -> None:
        comment: dict = CommentSchema().load(data)
        feature_id: str = comment["feature_id"] 
        message: str = comment["commentary"]

        feature: Feature = Feature.query.filter(Feature.external_id == feature_id).first()

        if feature is None:
            raise FeatureNotFoundException(f"Feature of external ID: {id} was not found")
        
        comment: Comment = Comment(commentary=message, feature_id=feature_id)

        database.session.add(comment)
        database.session.commit()

        response = CommentSchema().dump(Comment.query.get(comment.id))

        return response