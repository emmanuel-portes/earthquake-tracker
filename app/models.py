from sqlalchemy import  Column, NotNullable
from sqlalchemy import Integer, Identity, String, Numeric, Date

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Feature(Base):
    __tablename__ = 'features'

    id = Column("id", Integer, primary_key=True)
    type = Column("type", String(8), NotNullable)
    external_id = Column("external_id", String(15), unique=True)
    magnitude = Column("magnitude", Numeric(3,2), NotNullable)
    place = Column("place", String(100), NotNullable)
    event_date = Column("event_date", Date, NotNullable)
    url = Column("url", String(75), NotNullable)
    tsunami = Column("tsunami", Numeric(1,0), NotNullable)
    mag_type = Column("mag_type", String(2), NotNullable)
    title = Column("title", String(100), NotNullable)
    longitude = Column("longitude", Numeric(15, 7), NotNullable)
    latitude = Column("latitude", Numeric(15, 7), NotNullable)


class Comment(Base):
    __tablename__ = "comments"

    id = Column("id", Integer, primary_key=True)
    commentary = Column("commentary", String(100), NotNullable)
    feature_id = Column("feature_id", Integer)