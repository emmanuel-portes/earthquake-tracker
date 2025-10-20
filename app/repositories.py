from psycopg2 import DatabaseError, Error, IntegrityError
from models import Feature, Comment

class FeaturesRepository:
    
    def __init__(self, connection):
        self.connection = connection

    def get_features(self) -> list[Feature]:
        with self.connection as connection:
            with connection.cursor as cursor:
                cursor

    def get_feature_by_id(self, id: int) -> Feature:
        pass


class CommentsRepository:
    
    def __init__(self, connection):
        self.connection = connection

    def insert_comment(self, data: dict) -> None:
        pass

    def get_comments(self) -> list[Comment]:
        pass

    def get_comment_by_id(self, id: int) -> Comment:
        pass

    def get_comments_by_feature(self, feature: str) -> list[Comment]:
        pass