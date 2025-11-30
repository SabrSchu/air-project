from sqlalchemy import Column, Integer, ForeignKey, Float, String
from ..database.database import Base

""" -----------------------------------------------------------------------------------------------
 Database model for storing the corresponding metadata of a recommendation
----------------------------------------------------------------------------------------------- """


class Bm25Metadata(Base):
    __tablename__ = "bm25_metadata"

    id = Column(Integer, primary_key=True, index=True)
    score_raw = Column(Float)
    score_norm = Column(Float)
    score_percentile = Column(Float)
    rank = Column(Integer)
    matched_terms = Column(String(100))
    unmatched_terms = Column(String(100))
    max_matches = Column(Integer)
    match_count = Column(Integer)
    match_ratio = Column(Float)

    recommendation_id = Column(Integer, ForeignKey("recommendation.id"))
