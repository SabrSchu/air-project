from sqlalchemy.orm import Session
from app.models import UserSubmission, Recommendation, Plant, SbertMetadata, Bm25Metadata, UserPlantLike, UserAnswer, \
    Question, Answer
from app.schemas import RecommendationMetadataSBERT, Plant as PlantSchema, PlantMetadata, PlantRecommendation, \
    RecommendationMetadataBM25, UserInputQuestionnaire
from app.schemas.recommendations_schema import AllRecommendations, UserInput

""" -----------------------------------------------------------------------------------------------
 Query all plants including pagination
----------------------------------------------------------------------------------------------- """
def add_rating_to_recommendation(db: Session, submission_id: int, rating: int):
    submission_entry = db.query(UserSubmission).filter_by(id=submission_id).first()

    if not submission_entry:
        return None
    else:
        submission_entry.rating = rating

    db.commit()
    db.refresh(submission_entry)

    return submission_entry


""" -----------------------------------------------------------------------------------------------
 Collects all ever received recommendations and returns a list of it.
----------------------------------------------------------------------------------------------- """
def get_all_recommendations(db: Session, include_non_rated: bool):
    global metadata
    all_submissions_recs: list[AllRecommendations] = []
    all_submissions = db.query(UserSubmission).all()
    submission_type = ""

    for sub in all_submissions:

        # Skip not rated entries, just in case frontend wants some special logic
        if sub.rating is None and include_non_rated is False:
            continue

        recommendations = db.query(Recommendation).filter_by(submission_id=sub.id).all()

        recommendation_list: list = []
        for recom in recommendations:
            plant = db.query(Plant).filter_by(id=recom.plant_id).first()

            if recom.algorithm == 'sbert':
                submission_type = "free_text"
                metadata_sbert = db.query(SbertMetadata).filter_by(recommendation_id=recom.id).first()

                metadata = RecommendationMetadataSBERT(
                    algorithm="SBERT",
                    cosine_sim_raw=metadata_sbert.cosine_similarity_raw,
                    cosine_sim_normalized=metadata_sbert.cosine_similarity_norm,
                    rank=metadata_sbert.rank,
                    cosine_sim_percentile=metadata_sbert.cosine_similarity_percentile,
                    cosine_distance=metadata_sbert.cosine_distance,
                    gap_to_best=metadata_sbert.gap_to_best,
                )

            elif recom.algorithm == 'bm25':
                submission_type = "questionnaire"
                metadata_bm25 = db.query(Bm25Metadata).filter_by(recommendation_id=recom.id).first()

                metadata = RecommendationMetadataBM25(
                    score_raw=metadata_bm25.score_raw,
                    score_normalized=metadata_bm25.score_norm,
                    score_percentile=metadata_bm25.score_percentile,
                    rank=metadata_bm25.rank,
                    matched_terms=[metadata_bm25.matched_terms],
                    unmatched_terms=[metadata_bm25.unmatched_terms],
                    max_matches=metadata_bm25.max_matches,
                    match_count=metadata_bm25.match_count,
                    match_ratio=metadata_bm25.match_ratio
                )

            plant_metadata = PlantMetadata(
                **PlantSchema.model_validate(plant).model_dump(),
                metadata=metadata)

            recommendation_list.append(
                PlantRecommendation(
                    label=recom.label, # type: ignore
                    submission_id=recom.submission_id, # type: ignore
                    recommendation=[plant_metadata]))

        # Add user answers to the recommendation, such that frontend can display nicely
        user_answer = db.query(UserAnswer).filter_by(submission_id=sub.id).all()
        user_input_questionnaire_list = []
        user_input_free_text = ""

        if not user_answer:
            user_input_free_text = sub.free_text

        else:
            for answer in user_answer:
                question_id = answer.question_id
                answer_id = answer.answer_id

                question = db.query(Question).filter_by(id=question_id).first()
                answer = db.query(Answer).filter_by(id=answer_id).first()

                if question is not None and answer is not None:
                    question_type = question.type
                    question_text = question.question
                    answer_text = answer.answer

                    user_input_questionnaire_list.append(UserInputQuestionnaire(
                        question_type=question_type.value,
                        question=str(question_text),
                        answer=str(answer_text)
                    ))


        user_input = UserInput(
            type=submission_type,
            questionnaire=user_input_questionnaire_list,
            free_text=user_input_free_text
        )

        all_submissions_recs.append(
            AllRecommendations(
                submission_id=sub.id, # type: ignore
                rating=sub.rating,  # type: ignore
                user_input=user_input,
                recommendations_per_submission=recommendation_list # type: ignore
            )
        )
    return all_submissions_recs


""" -----------------------------------------------------------------------------------------------
 Clears all user specific data. Used especially in testing and development phase
----------------------------------------------------------------------------------------------- """
def delete_all_entries(db: Session):

    db.query(Bm25Metadata).delete()
    db.query(SbertMetadata).delete()
    db.query(Recommendation).delete()
    db.query(UserPlantLike).delete()
    db.query(UserSubmission).delete()
    db.query(UserAnswer).delete()

    db.commit()
