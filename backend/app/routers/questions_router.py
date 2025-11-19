from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.base import state_str
from starlette import status
from starlette.status import HTTP_400_BAD_REQUEST
from ..database.database import get_db
from ..schemas import Question, PlantRecommendation, UserAnswerSubmission, UserFreeTextSubmission
from ..services import question_service
from ..recommender import recommender_placeholder, bm25_recommender


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
        questionnaire: UserAnswerSubmission,
        num_perfect_fits: int = Query(default=3, ge=0, le=10, description="Number perfect fits to receive"),
        num_good_fits: int = Query(default=3, ge=0, le=10, description="Number of good fits to receive"),
        num_bad_fits: int = Query(default=3, ge=0, le=10, description="Number of mismatches to receive"),
        db: Session = Depends(get_db)):

    """
    Send your quiz answers to receive a recommendation. You can choose a variable number of recommendations
    for perfect fits, good fits or mismatches!
    """

    # First step input validation, all 5 questions must be answered
    try:
        question_service.validate_questionnaire(user_answers=questionnaire)

    except ValueError as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))

    # Then storing the answers to database, for further use later (e.g. evaluations)
    question_service.store_user_answers(user_answers=questionnaire, db=db)


    # Calling the recommender, fixme for now only placeholder until we have a final model

    result = bm25_recommender.get_recommendations(num=num_perfect_fits, user_answers=questionnaire, db=db)

    #perfect_fit = recommender_placeholder.get_perfect_recommendations(num=num_perfect_fits, user_answers=questionnaire, db=db)
    #good_fit = recommender_placeholder.get_good_recommendations(num=num_good_fits, user_answers=questionnaire, db=db)
    #mismatch = recommender_placeholder.get_mismatches(num=num_bad_fits, user_answers=questionnaire, db=db)

    return [result, result, result]


""" -----------------------------------------------------------------------------------------------
 Endpoint that takes a free text from the user, sanitizes it, stores it in the database, activates 
 the recommender algorithm, and returns a list of recommendations.
----------------------------------------------------------------------------------------------- """
@question_router.post("/free_text",
                      summary="Post free text from the user, and receive variable number of recommendations",
                      response_model=list[PlantRecommendation],
                      status_code=status.HTTP_201_CREATED)

def post_free_text_receive_recommendation(
        user_submission: UserFreeTextSubmission,
        num_perfect_fits: int = Query(default=3, ge=0, le=10, description="Number perfect fits to receive"),
        num_good_fits: int = Query(default=3, ge=0, le=10, description="Number of good fits to receive"),
        num_bad_fits: int = Query(default=3, ge=0, le=10, description="Number of mismatches to receive"),
        db: Session = Depends(get_db)):

    """
    Send the user's free text (max. 300 chars) to receive a recommendation based on this. You can choose a variable number of
    recommendations for perfect fits, good fits or mismatches!
    """

    try:
        question_service.store_user_submission(user_submission=user_submission, db=db)

    except:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="DB error!")

    # Calling the recommender, fixme for now only placeholder until we have a final model

    perfect_fit = recommender_placeholder.get_perfect_recommendations_free_text(num=num_perfect_fits, user_submission=user_submission, db=db)
    good_fit = recommender_placeholder.get_good_recommendations_free_text(num=num_good_fits, user_submission=user_submission, db=db)
    mismatch = recommender_placeholder.get_mismatches_free_text(num=num_bad_fits, user_submission=user_submission, db=db)

    return [perfect_fit, good_fit, mismatch]