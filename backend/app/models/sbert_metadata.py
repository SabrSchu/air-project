from sqlalchemy import Column, Integer, ForeignKey, Enum, Float
from ..database.database import Base
from ..enums import Algorithm
from ..enums.recommendation import Label

""" -----------------------------------------------------------------------------------------------
 Database model for storing the corresponding metadata of a recommendation
----------------------------------------------------------------------------------------------- """


class SbertMetadata(Base):
    __tablename__ = "sbert_metadata"

    id = Column(Integer, primary_key=True, index=True)

    cosine_similarity_raw = Column(Float)
    cosine_similarity_norm = Column(Float)
    cosine_similarity_percentile = Column(Float)
    rank = Column(Integer)
    cosine_distance = Column(Float)
    gap_to_best = Column(Float)

    recommendation_id = Column(Integer, ForeignKey("recommendation.id"))