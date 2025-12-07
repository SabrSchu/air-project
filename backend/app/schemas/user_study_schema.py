from pydantic import BaseModel
from datetime import datetime


""" -----------------------------------------------------------------------------------------------
 Schema for single user study answer item
----------------------------------------------------------------------------------------------- """
class UserStudyAnswerItem(BaseModel):
    section_id: int
    item_id: int
    rating: int |  None = None
    free_text: str | None = None


""" -----------------------------------------------------------------------------------------------
 Schema for request format of user study answers
----------------------------------------------------------------------------------------------- """
class UserStudySubmission(BaseModel):
    user_name: str
    created_at: datetime
    user_study_answers: list[UserStudyAnswerItem]


""" -----------------------------------------------------------------------------------------------
 Schema for standard response message
----------------------------------------------------------------------------------------------- """
class UserStudySubmitted(BaseModel):
    detail: str