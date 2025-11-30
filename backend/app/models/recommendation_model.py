from sqlalchemy import Column, Integer, ForeignKey, Enum
from ..database.database import Base
from ..enums import Algorithm
from ..enums.recommendation import Label

""" -----------------------------------------------------------------------------------------------
 Database model for storing returned recommendations
----------------------------------------------------------------------------------------------- """


class Recommendation(Base):
    __tablename__ = "recommendation"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(Enum(Label))
    algorithm = Column(Enum(Algorithm))

    plant_id = Column(Integer, ForeignKey("plants.id"))
    submission_id = Column(Integer, ForeignKey("user_submission.id"))
