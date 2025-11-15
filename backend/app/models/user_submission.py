from sqlalchemy import Column, Integer, DateTime, String
from ..database.database import Base

""" -----------------------------------------------------------------------------------------------
 Database model for having one submission that holds the free text answer plus structured user
 answers
----------------------------------------------------------------------------------------------- """


class UserSubmission(Base):
    __tablename__ = "user_submission"

    id = Column(Integer, primary_key=True, index=True)
    free_text = Column(String(300))
    created_at = Column(DateTime)