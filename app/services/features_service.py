from app import database

from app.models.features_model import Feature
from app.models.comments_model import Comment

from app.schemas.feature_schema import FeatureSchema
from app.schemas.comment_schema import CommentSchema

from app.exceptions import FeatureNotFoundException

class FeatureService:

    def get_features(self, page:int = 1, number_of_items:int = 10,  mag_type: str = None) -> dict[dict]:
        if mag_type is None:
            data: list = Feature.query.order_by(Feature.event_date.desc()).paginate(page=page, per_page=number_of_items)

        if mag_type is not None:
            data: list = Feature.query.filter(Feature.mag_type == mag_type).order_by(Feature.event_date.desc()).paginate(page=page, per_page=number_of_items)
            
        features:list[FeatureSchema] = FeatureSchema(many=True).dump(data.items)
        pagination: dict = {"current_page": data.page, "total": data.total, "per_page": data.per_page}
        result: dict = {"data": features, "pagination": pagination}
        return result
    
    def get_feature_by_code(self, code: int) -> dict:
        data: Feature | None = Feature.query.filter(Feature.code == code).first()
        if data is None:
            raise FeatureNotFoundException(f"Feature of ID: {code} was not found")
        feature: FeatureSchema = FeatureSchema().dump(data)
        return feature
        
    def get_feature_by_usgs_code(self, usgs_code: str) -> dict:
        data: Feature | None = Feature.query.filter(Feature.usgs_code == usgs_code).first()
        if data is None:
            raise FeatureNotFoundException(f"Feature of external ID: {usgs_code} was not found")
        feature: dict = FeatureSchema().dump(data)
        return feature

    def save_feature_comment(data:dict[str,str]) -> None:
        comment: dict = CommentSchema().load(data)
        usgs_code: str = comment["usgs_code"] 
        message: str = comment["comment"]

        feature: Feature = Feature.query.filter(Feature.usgs_code == usgs_code).first()

        if feature is None:
            raise FeatureNotFoundException(f"Feature of external ID: {usgs_code} was not found")
        
        comment: Comment = Comment(comment=message, usgs_code=usgs_code)

        database.session.add(comment)
        database.session.commit()

        response = CommentSchema().dump(Comment.query.get(comment.id))

        return response