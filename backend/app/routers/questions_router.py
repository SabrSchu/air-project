from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from starlette import status
from ..database.database import get_db
from ..schemas import Question, PlantRecommendation, UserAnswer
from ..services import question_service


question_router = APIRouter(prefix="/questions", tags=["Questions"])


""" -----------------------------------------------------------------------------------------------
 Simple endpoint that returns all available questions and the answer options.
----------------------------------------------------------------------------------------------- """
@question_router.get("/all",
                 summary="Get all Questions with Answer Options",
                 response_model=list[Question],
                 status_code=status.HTTP_200_OK)

def get_all_questions(db: Session = Depends(get_db)):

    """
    Get all available questions with the corresponding answers
    """

    all_questions = question_service.fetch_all_questions(db=db)
    return all_questions


""" -----------------------------------------------------------------------------------------------
 Endpoint that takes the user answers, stores it in the database, activates the recommender 
 algorithm, and returns a list of recommendations.
----------------------------------------------------------------------------------------------- """
@question_router.post("/",
                      summary="Post questionnaire, receive variable number of recommendations",
                      response_model=list[PlantRecommendation],
                      status_code=status.HTTP_201_CREATED)

def post_questions_receive_recommendation(
        questionnaire: list[UserAnswer],
        num_perfect_fits: int = Query(default=3, ge=0, le=10, description="Number perfect fits to receive"),
        num_good_fits: int = Query(default=3, ge=0, le=10, description="Number of good fits to receive"),
        num_bad_fits: int = Query(default=3, ge=0, le=10, description="Number of mismatches to receive"),
        db: Session = Depends(get_db)):

    """
    Send your quiz answers to receive a recommendation. You can choose a variable number of recommendations
    for perfect fits, good fits or mismatches!
    """

    perfect_fit = question_service.get_perfect_recommendations(num=num_perfect_fits, user_answers=questionnaire, db=db)

    good_fit = question_service.get_good_recommendations(num=num_good_fits, user_answers=questionnaire, db=db)

    mismatch = question_service.get_mismatches(num=num_bad_fits, user_answers=questionnaire, db=db)

    return "todo"