from sqlalchemy import Column, Integer, DateTime, ForeignKey
from ..database.database import Base

""" -----------------------------------------------------------------------------------------------
 Database model for tracking specific user entries
----------------------------------------------------------------------------------------------- """


class UserAnswer(Base):
    __tablename__ = "user_answer"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("question.id"))
    answer_id = Column(Integer, ForeignKey("answer.id"))
    submission_id = Column(Integer, ForeignKey("user_submission.id"))
