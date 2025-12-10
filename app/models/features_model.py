
from sqlalchemy import Integer, String, Numeric, Date, Boolean
from sqlalchemy.orm import Mapped, mapped_column, WriteOnlyMapped, relationship

from app import database

class Feature(database.Model):
    __tablename__ = 'features'

    code: Mapped[int] = mapped_column(Integer, primary_key=True)
    usgs_class: Mapped[str] = mapped_column(String(8), nullable=False)
    usgs_code: Mapped[str] = mapped_column( String(15), unique=True)
    magnitude: Mapped[float] = mapped_column(Numeric(4,2), nullable=False)
    place: Mapped[str] = mapped_column( String(100), nullable=False)
    event_date: Mapped[Date]  = mapped_column( Date, nullable=False)
    url: Mapped[str] = mapped_column(String(75), nullable=False)
    tsunami: Mapped[int] = mapped_column(Boolean, nullable=False)
    mag_type: Mapped[str] = mapped_column(String(3), nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    longitude: Mapped[float] = mapped_column( Numeric(15, 7), nullable=False)
    latitude: Mapped[float] = mapped_column( Numeric(15, 7), nullable=False)

    comments: WriteOnlyMapped['Comment'] = relationship("Comment", back_populates='feature')

    def __repr__(self) -> str:
        return f"Feature({self.usgs_code} - {self.code})"
    
from app.models.comments_model import Comment