from sqlalchemy.orm import Session
from ..schemas import UserAnswerSubmission, PlantRecommendation, UserFreeTextSubmission
from ..services import recommender_placeholder_service


""" -----------------------------------------------------------------------------------------------
 Placeholder Recommender, for now returns random results. Later on here we will add the
 proper algorithm.
----------------------------------------------------------------------------------------------- """

def get_perfect_recommendations(num: int, user_answers: UserAnswerSubmission, db: Session):
    plant_list = recommender_placeholder_service.fetch_plant_recommendations_randomly(num_plants=num, db=db)

    return PlantRecommendation (
        label="perfect",
        recommendation=plant_list
    )


def get_good_recommendations(num: int, user_answers: UserAnswerSubmission, db:Session):
    good_plant_list = recommender_placeholder_service.fetch_plant_recommendations_randomly(num_plants=num, db=db)

    return PlantRecommendation (
        label="good",
        recommendation=good_plant_list
    )


def get_mismatches(num: int, user_answers: UserAnswerSubmission, db: Session):
    mismatch_list = recommender_placeholder_service.fetch_plant_recommendations_randomly(num_plants=num, db=db)

    return PlantRecommendation (
        label="mismatch",
        recommendation=mismatch_list
    )


""" -----------------------------------------------------------------------------------------------
 Placeholder Recommender for free text, for now returns random results. Later on here we will add the
 proper algorithm.
----------------------------------------------------------------------------------------------- """

def get_perfect_recommendations_free_text(num: int, user_submission: UserFreeTextSubmission, db: Session):
    plant_list = recommender_placeholder_service.fetch_plant_recommendations_randomly(num_plants=num, db=db)

    return PlantRecommendation (
        label="perfect",
        recommendation=plant_list
    )


def get_good_recommendations_free_text(num: int, user_submission: UserFreeTextSubmission, db:Session):
    good_plant_list = recommender_placeholder_service.fetch_plant_recommendations_randomly(num_plants=num, db=db)

    return PlantRecommendation (
        label="good",
        recommendation=good_plant_list
    )


def get_mismatches_free_text(num: int, user_submission: UserFreeTextSubmission, db: Session):
    mismatch_list = recommender_placeholder_service.fetch_plant_recommendations_randomly(num_plants=num, db=db)

    return PlantRecommendation (
        label="mismatch",
        recommendation=mismatch_list
    )