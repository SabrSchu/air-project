from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.status import HTTP_400_BAD_REQUEST
from ..database.database import get_db
from ..recommender.SBERT.sbert_recommender import SBertRecommender
from ..schemas import Question, PlantRecommendation, UserAnswerSubmission, UserFreeTextSubmission
from ..services import question_service
from ..recommender.BM25 import BM25Recommender

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

    try:
        # First step input validation, all 5 questions must be answered
        question_service.validate_questionnaire(user_answers=questionnaire)

        # Then storing the answers to database, for further use later (e.g. evaluations)
        submission_id = question_service.store_user_answers(user_answers=questionnaire, db=db)

        # Initializing and calling recommender, Here BM25 is used
        bm25_recommender = BM25Recommender(db=db, submission_id=submission_id)

        # Doing the actual recommendation - yay
        return bm25_recommender.recommend(user_answers=questionnaire,
                                          num_perfect=num_perfect_fits,
                                          num_good=num_good_fits,
                                          num_bad=num_bad_fits)

    except ValueError as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))





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
        submission_id = question_service.store_user_submission(user_submission=user_submission, db=db)

        # Initializing the SBERT recommender class
        s_bert_recommender = SBertRecommender(db=db, submission_id=submission_id)

        # Do the actual recommendation
        return s_bert_recommender.recommend(user_free_text=user_submission,
                                            num_perfect=num_perfect_fits,
                                            num_good=num_good_fits,
                                            num_bad=num_bad_fits)

    except:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Unexpected Error!")







