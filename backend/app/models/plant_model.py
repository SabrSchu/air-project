from sqlalchemy import Column, Integer, String
from ..database.database import Base

""" -----------------------------------------------------------------------------------------------
 Database model for Plant entries
----------------------------------------------------------------------------------------------- """
class Plant(Base):
    __tablename__ = "plants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(32), index=True)
    growth = Column(String(32), nullable=False)
    soil = Column(String(32), nullable=False)
    sunlight = Column(String(32), nullable=False)
    watering = Column(String(64), nullable=False)
    fertilization = Column(String(32), nullable=False)
    image_url = Column(String(128), nullable=True)
