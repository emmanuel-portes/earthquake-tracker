from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import database

from app.models.features_model import Feature

class Comment(database.Model):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    comment: Mapped[str] = mapped_column(Text, nullable=False)
    usgs_code: Mapped[str] = mapped_column(String(15), ForeignKey("features.usgs_code"))
    feature: Mapped[Feature] = relationship(back_populates='comments')

    def __repr__(self):
        return f"Comment({self.id} - {self.usgs_code}>"
    
