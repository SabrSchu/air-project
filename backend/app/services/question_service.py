from sqlalchemy.orm import Session, joinedload
from app.models import Question
from app.schemas import UserAnswer

""" -----------------------------------------------------------------------------------------------
 Query all questions and the corresponding answer options
----------------------------------------------------------------------------------------------- """
def fetch_all_questions(db: Session) -> list[type[Question]]:
    questions = db.query(Question).options(joinedload(Question.answer_option)).all()
    return questions


def store_user_answers(db: Session):
    pass

def get_perfect_recommendations(num: int, user_answers: list[UserAnswer], db: Session):
    pass

def get_good_recommendations(num: int, user_answers: list[UserAnswer], db:Session):
    pass

def get_mismatches(num: int, user_answers: list[UserAnswer], db: Session):
    pass