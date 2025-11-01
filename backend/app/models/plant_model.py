from sqlalchemy import Column, Integer, String, Float, Boolean
from ..database.database import Base

class Plant(Base):
    __tablename__ = "plants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    growth = Column(String, nullable=False)
    soil = Column(String, nullable=False)
    sunlight = Column(String, nullable=False)
    watering = Column(String, nullable=False)
    fertilization = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    liked = Column(Boolean, default=False)