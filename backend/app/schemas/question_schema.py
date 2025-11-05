from pydantic import BaseModel
from app.enums import QuestionType
from .answer_schema import Answer

""" -----------------------------------------------------------------------------------------------
 Schema for response format of questions and corresponding list of possible answers
----------------------------------------------------------------------------------------------- """
class Question(BaseModel):
    id: int
    type: QuestionType
    question: str
    answer_option: list[Answer]

    class Config:
        from_attributes = True


