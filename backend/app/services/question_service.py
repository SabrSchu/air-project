from sqlalchemy.orm import Session, joinedload
from app.models import Question
from app.schemas import UserAnswer
from app.models import UserAnswer as UserAnswerModel


""" -----------------------------------------------------------------------------------------------
 Query all questions and the corresponding answer options
----------------------------------------------------------------------------------------------- """
def fetch_all_questions(db: Session) -> list[type[Question]]:
    questions = db.query(Question).options(joinedload(Question.answer_option)).all()
    return questions


""" -----------------------------------------------------------------------------------------------
 Helper that stores the user answers to the database. Each questionnaire is unique by datetime.
----------------------------------------------------------------------------------------------- """
def store_user_answers(user_answers: list[UserAnswer], db: Session):

    for user_answer in user_answers:
        answer = {
            "question_id": user_answer.question_id,
            "answer_id": user_answer.answer_id,
            "created_at": user_answer.created_at
        }

        db.add(UserAnswerModel(question_id=answer["question_id"],
                               answer_id=answer["answer_id"],
                               created_at=answer["created_at"]))

    db.commit()


""" -----------------------------------------------------------------------------------------------
 Helper makes sure that all questions are correctly sent from the frontend.
----------------------------------------------------------------------------------------------- """
def validate_questionnaire(user_answers: list[UserAnswer]):

    # Checking validity of questions
    if len(user_answers) < 5:
        raise ValueError(f"Error! You must send all 5 answers!")

    if len(user_answers) > 5:
        raise ValueError(f"Error! Too many answers!")

    required_question_ids = {1, 2, 3, 4, 5}
    actual_present_ids = [element.question_id for element in user_answers]

    if not required_question_ids.issubset(actual_present_ids):
        raise ValueError(f"Error! Not all questions are answered!")

    # Checking validity of provided answers, they must match the question.
    correct_answer_ids = {
        1: {1, 2, 3, 4},
        2: {5, 6, 7},
        3: {8, 9, 10, 11, 12, 13},
        4: {14, 15, 16},
        5: {17, 18, 19, 20}
    }

    for answer in user_answers:
        valid_ids = correct_answer_ids.get(answer.question_id)

        if valid_ids is None or answer.answer_id not in valid_ids:
            raise ValueError(f"Error! Invalid answer_id for question: {answer.question_id}. "
                             f"Call the endpoint GET /questions/all to check which answer_ids are valid!")
