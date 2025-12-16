from typing import Optional
from pydantic import BaseModel
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
 Schema for response format of user answers for recommendation
----------------------------------------------------------------------------------------------- """
class UserInputQuestionnaire(BaseModel):
    question_type: str
    question: str
    answer: str


""" -----------------------------------------------------------------------------------------------
 Schema for response format of user answers for recommendation
----------------------------------------------------------------------------------------------- """
class UserInput(BaseModel):
    type: str
    free_text: Optional[str] = None
    questionnaire: Optional[list[UserInputQuestionnaire]] = None


""" -----------------------------------------------------------------------------------------------
 Schema for response format of all ever returned recommendations
----------------------------------------------------------------------------------------------- """
class AllRecommendations(BaseModel):
    submission_id: int
    rating: int | None
    user_input: UserInput
    recommendations_per_submission: list[PlantRecommendation]


""" -----------------------------------------------------------------------------------------------
 Schema for standard response message
----------------------------------------------------------------------------------------------- """
class DeleteMetadataResponse(BaseModel):
    detail: str
