from models.features_model import Feature

from schemas.feature_schema import FeatureSchema

class FeatureService:

    def get_features(self) -> list[FeatureSchema]:
        data: list[Feature] = Feature.query.all()
        features:list[FeatureSchema] = FeatureSchema(many=True).dump(data)
        return features
    
    