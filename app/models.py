from sqlalchemy import NotNullable
from sqlalchemy import Integer, String, Numeric, Date
from sqlalchemy.orm import Mapped, mapped_column, WriteOnlyMapped, relationship

from app import database

class Feature(database.Model):
    __tablename__ = 'features'

    feature_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    feature_type: Mapped[str] = mapped_column(String(8), NotNullable)
    external_id: Mapped[str] = mapped_column( String(15), unique=True)
    magnitude: Mapped[float] = mapped_column(Numeric(3,2), NotNullable)
    place: Mapped[str] = mapped_column( String(100), NotNullable)
    event_date: Mapped[Date]  = mapped_column( Date, NotNullable)
    url: Mapped[str] = mapped_column(String(75), NotNullable)
    tsunami: Mapped[int] = mapped_column(Numeric(1,0), NotNullable)
    mag_type: Mapped[str] = mapped_column(String(2), NotNullable)
    title: Mapped[str] = mapped_column(String(100), NotNullable)
    longitude: Mapped[float] = mapped_column( Numeric(15, 7), NotNullable)
    latitude: Mapped[float] = mapped_column( Numeric(15, 7), NotNullable)

    comments: WriteOnlyMapped['Comment'] = relationship(back_populates='feature')

    def __repr__(self):
        return f"Feature({self.external_id} - {self.feature_id})"

class Comment(database.Model):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    commentary: Mapped[str] = mapped_column(String(100), NotNullable)
    feature_id: Mapped[int] = mapped_column(Integer)
    feature: Mapped[Feature] = relationship(back_populates='comments')

    def __repr__(self):
        return f"Comment({self.id} - {self.feature_id}>"