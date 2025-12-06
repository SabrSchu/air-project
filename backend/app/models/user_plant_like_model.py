from sqlalchemy import Column, Integer, ForeignKey
from ..database.database import Base

""" -----------------------------------------------------------------------------------------------
 Database model for storing info about liked plants
----------------------------------------------------------------------------------------------- """
class UserPlantLike(Base):
    __tablename__ = "user_plant_like"

    id = Column(Integer, primary_key=True, index=True)
    like_counter = Column(Integer)

    plant_id = Column(Integer, ForeignKey("plants.id"))