from sqlalchemy import Column, Integer, String, Enum, orm, ForeignKey
from ..database.database import Base
from ..enums import QuestionType

""" -----------------------------------------------------------------------------------------------
 Database model for Answer entries
----------------------------------------------------------------------------------------------- """
class Answer(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(QuestionType))
    answer = Column(String(64), nullable=False)
    question_id = Column(Integer, ForeignKey("question.id"))

    user_answer = orm.relationship("UserAnswer")