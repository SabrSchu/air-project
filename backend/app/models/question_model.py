from sqlalchemy import Column, Integer, String, Enum, orm
from ..database.database import Base
from ..enums import QuestionType

""" -----------------------------------------------------------------------------------------------
 Database model for Question entries
----------------------------------------------------------------------------------------------- """
class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(QuestionType))
    question = Column(String(300), nullable=False)

    answer_option = orm.relationship("Answer")
    user_answer = orm.relationship("UserAnswer")
