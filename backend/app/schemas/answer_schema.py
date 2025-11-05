from pydantic import BaseModel
from datetime import datetime

""" -----------------------------------------------------------------------------------------------
 Schema for response format of one answer option
----------------------------------------------------------------------------------------------- """
class Answer(BaseModel):
    id: int
    answer: str

    class Config:
        from_attributes = True


class UserAnswer(BaseModel):
    question_id: int
    answer_id: int
    created_at: datetime