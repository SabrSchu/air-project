from pydantic import BaseModel, Field
from datetime import datetime

from app.schemas import PlantRecommendation

""" -----------------------------------------------------------------------------------------------
 Schema for response format of recommendation rating
----------------------------------------------------------------------------------------------- """
class RecommendationRatingResponse(BaseModel):
    submission_id: int
    created_at: datetime
    rating: int


""" -----------------------------------------------------------------------------------------------
 Schema for response format of all ever returned recommendations
----------------------------------------------------------------------------------------------- """
class AllRecommendations(BaseModel):
    submission_id: int
    rating: int | None
    recommendations_per_submission: list[PlantRecommendation]


""" -----------------------------------------------------------------------------------------------
 Schema for standard response message
----------------------------------------------------------------------------------------------- """
class DeleteMetadataResponse(BaseModel):
    detail: str
