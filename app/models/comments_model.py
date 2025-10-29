from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import database

from app.models.features_model import Feature

class Comment(database.Model):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    commentary: Mapped[str] = mapped_column(Text, nullable=False)
    feature_id: Mapped[str] = mapped_column(String(15), ForeignKey("features.external_id"))
    feature: Mapped[Feature] = relationship(back_populates='comments')

    def __repr__(self):
        return f"Comment({self.id} - {self.feature_id}>"
    
