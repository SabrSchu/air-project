from pydantic import BaseModel, Field
from datetime import datetime

""" -----------------------------------------------------------------------------------------------
 Schema for response format of one answer option
----------------------------------------------------------------------------------------------- """
class Answer(BaseModel):
    id: int
    answer: str

    class Config:
        from_attributes = True


""" -----------------------------------------------------------------------------------------------
 Schema for user answers of the questionnaire, each question has one answer (right now)
----------------------------------------------------------------------------------------------- """
class UserAnswer(BaseModel):
    question_id: int
    answer_id: int

""" -----------------------------------------------------------------------------------------------
 Schema for one submission that holds a list of user answers plus the free text field
----------------------------------------------------------------------------------------------- """
class UserAnswerSubmission(BaseModel):
    answers: list[UserAnswer]
    created_at: datetime
    free_text: str | None = Field(default=None, max_length=300)