import random
import numpy as np
from sqlalchemy.orm import Session
from app.models import Plant, Answer, Question, Bm25Metadata, Recommendation
from app.schemas import UserAnswerSubmission, Plant as PlantSchema, PlantMetadata
from .bm25_mappings import DB_ANSWER_MAPPING_GROWTH, DB_ANSWER_MAPPING_WATER, DB_ANSWER_MAPPING_SOIL, \
                      DB_ANSWER_MAPPING_SUN, DB_ANSWER_MAPPING_FERTILIZER
from app.schemas import RecommendationMetadataBM25

""" -----------------------------------------------------------------------------------------------
 Helper the creates a "corpus" for the BM25 model. This is a preprocessing step. It takes each
 row of the database, and makes one big string out of it. It also prepends the "<column_name>_" 
 to have unique entries for making the classical keyword search of BM25 possible.
 Returns the plant corpus.
----------------------------------------------------------------------------------------------- """
def create_plant_corpus(db: Session) -> list[str]:
    all_plants = db.query(Plant).all()
    plant_corpus: list = []

    for plant in all_plants:

        concat_line = " ".join([
            str(plant.id),
            str(plant.name).replace(" ", "_"),
            "growth_" + DB_ANSWER_MAPPING_GROWTH[str(plant.growth)],
            "soil_" + DB_ANSWER_MAPPING_SOIL[str(plant.soil)],
            "water_" + DB_ANSWER_MAPPING_WATER[str(plant.watering)],
            "sun_" + DB_ANSWER_MAPPING_SUN[str(plant.sunlight)],
            "fertilizer_" + DB_ANSWER_MAPPING_FERTILIZER[str(plant.fertilization)]
            ]
        )
        plant_corpus.append(concat_line)

    return plant_corpus


""" -----------------------------------------------------------------------------------------------
 Builds a query based on the user questionnaire. The answers are mapped to the specific db entries.
 "Don't care" answers are ignored, and free text is also ignored here, because BM25 does keyword
 search, and we changed the corpus in regards of customizing it to make entries unique.
 Returns the query as string.
----------------------------------------------------------------------------------------------- """
def create_query(db: Session, user_answers: UserAnswerSubmission) -> str:

    user_query: list = []

    for answer in user_answers.answers:
        question = db.query(Question).filter_by(id=answer.question_id).first()
        answer = db.query(Answer).filter_by(id=answer.answer_id).first()

        plant_type = str(question.type.value)
        ans_value = str(answer.answer)

        if ans_value != "don't care":
            user_query.append(f"{str(plant_type)}_{str(ans_value)}")

    clean_preprocessed_user_query = " ".join(user_query)

    return clean_preprocessed_user_query


""" -----------------------------------------------------------------------------------------------
 The BM25 returns the documents that fit the best. This helper method extracts the plant id from
 the documents, and searches for the plants based on this id in the db. It also calculates metadata
 for each recommendation and stores it in the database.
 Returns list of Plants, which are the base for a Plant recommendation. Plant entries with image
 url are preferred.
----------------------------------------------------------------------------------------------- """
def get_plant_based_on_bm25_document(db: Session,
                                     results: list, max_results: int, all_scores: list,
                                     tokenized_query: list, submission_id: int, label: str) -> list[PlantMetadata]:
    all_recommendations: list = []
    final_recommendations: list = []

    ranks = map_scores_to_rank(all_scores=all_scores)

    for doc in results:
        doc_text, score = doc[:2]
        plant_id = doc_text.split(" ")[0]

        # Get plant from db per id
        plant = db.query(Plant).filter_by(id=plant_id).first()
        plant_schema = PlantSchema.model_validate(plant)

        # Calculate metadata
        score_norm = calculate_min_max_normalization(all_scores=all_scores, score=score)
        score_percentile = get_score_percentile(all_scores=all_scores, score=score)
        plant_tokens = doc_text.split()[2:]
        matched, unmatched = get_matched_and_unmatched_terms(query=tokenized_query, document=plant_tokens)

        plant_metadata = RecommendationMetadataBM25(score_raw=round(score, 4),
                                                    score_normalized=score_norm,
                                                    score_percentile=score_percentile,
                                                    rank=ranks[score],
                                                    matched_terms=matched,
                                                    unmatched_terms=unmatched,
                                                    max_matches=len(plant_tokens),
                                                    match_count=len(matched),
                                                    match_ratio=round(len(matched) / (len(plant_tokens)), 2))

        # Building the recommendation with the plant itself + metadata
        plant_recommendation = PlantMetadata(**plant_schema.model_dump(), metadata=plant_metadata)

        # Preferring those with image present, store metadata in db, return final recommendations
        all_recommendations.append((plant_recommendation, bool(plant.image_url != "")))
        all_recommendations.sort(key=lambda x: not x[1])
        final_recommendations = [recom for (recom, img_url) in all_recommendations[:max_results]]

    # Store in db for later use
    store_recommendation_and_metadata_to_db(db=db,
                                            sub_id=submission_id,
                                            label=label,
                                            recommendations=final_recommendations)

    return final_recommendations


""" -----------------------------------------------------------------------------------------------
 Additionally to finding "perfect fits" we also want to return "moderate good fits" and "mismatches".
 For that we take the scores returned by the BM25 (each score corresponds to a plant entry in the
 corpus), and manually choose the percentile of the fit we want to get. Mismatches are in the lowest
 percentiles, moderate/good fits we search in the 70th-90th percentile.
----------------------------------------------------------------------------------------------- """
def get_fits_in_percentile(scores: list, dataset_corpus: list, n: int, min_p: int, max_p: int) -> list[
    tuple[str, float]]:
    p1_threshold = np.percentile(scores, min_p)
    p2_threshold = np.percentile(scores, max_p)

    candidates = np.where((scores >= p1_threshold) & (scores <= p2_threshold))[0]

    # Necessary because np and array format problems in case there are too little results
    candidates = np.atleast_1d(candidates).tolist()

    # if more than the requested num of results are found, choose randomly
    if len(candidates) > n:
        random_n = random.sample(candidates, k=n)
    else:
        random_n = candidates

    # basic search per index
    good_fits: list[tuple[str, float]] = []
    for element in random_n:
        good_fits.append((dataset_corpus[element], scores[element]))

    return good_fits


""" -----------------------------------------------------------------------------------------------
 Normalizes the raw score for easier comparison. Method Min-Max normalization oriented on:
 https://www.codecademy.com/article/min-max-zscore-normalization
----------------------------------------------------------------------------------------------- """
def calculate_min_max_normalization(all_scores: list, score: float) -> float:
    minimum = min(all_scores)
    maximum = max(all_scores)

    normalized_score = (score - minimum) / (maximum - minimum)

    return round(normalized_score, 2)


""" -----------------------------------------------------------------------------------------------
 Maps scores to ranks, returns a dictionary with key value pairs of {score: rank}
----------------------------------------------------------------------------------------------- """
def map_scores_to_rank(all_scores: list) -> dict[float, int]:
    sorted_scores = sorted(all_scores, reverse=True)

    score_and_rank = {}
    rank = 1
    for score in sorted_scores:
        if score not in score_and_rank:
            score_and_rank[score] = rank
        rank += 1

    return score_and_rank


""" -----------------------------------------------------------------------------------------------
 Calculates the percentile position of the score. Eg. if the percentile rank of the current score
 is 0.6, this means that the current score is higher than 60% of all scores in the list
----------------------------------------------------------------------------------------------- """
def get_score_percentile(all_scores: list, score: float) -> float:

    num_scores_below_target = sum(1 for s in all_scores if s < score)
    percentile_rank = (num_scores_below_target / len(all_scores))

    return round(percentile_rank, 3)


""" -----------------------------------------------------------------------------------------------
 Returns all terms that match and unmatch the document tokens based on the user query
----------------------------------------------------------------------------------------------- """
def get_matched_and_unmatched_terms(query: list, document: list) -> tuple[list, list]:

    matched_terms: list = []
    unmatched_terms: list = []

    for term in document:
        if term in query:
            matched_terms.append(term)
        else:
            unmatched_terms.append(term)

    return matched_terms, unmatched_terms


""" -----------------------------------------------------------------------------------------------
 Helper for storing recommendation data in database. Returns recommendation id for metadata table.
----------------------------------------------------------------------------------------------- """
def store_bm25_recommendation_in_db(db: Session, sub_id: int, label: str, plant_id: int) -> int:

    recommendation = Recommendation(label=label,
                          algorithm="bm25",
                          plant_id=plant_id,
                          submission_id=sub_id)

    db.add(recommendation)
    db.flush()
    db.commit()

    return recommendation.id


""" -----------------------------------------------------------------------------------------------
 Helper for storing metadata of each recommendation in database.
----------------------------------------------------------------------------------------------- """
def store_bm25_metadata_in_db(db: Session, metadata: RecommendationMetadataBM25, rec_id: int):

    db.add(Bm25Metadata(score_raw=round(metadata.score_raw, 4),
                        score_norm=metadata.score_normalized,
                        score_percentile=metadata.score_percentile,
                        rank=metadata.rank,
                        matched_terms=str(metadata.matched_terms),
                        unmatched_terms=str(metadata.unmatched_terms),
                        max_matches=metadata.max_matches,
                        match_count=metadata.match_count,
                        match_ratio=metadata.match_ratio,
                        recommendation_id=rec_id))

    db.commit()


""" -----------------------------------------------------------------------------------------------
 Helper for storing both, metadata and recommendation data in the db. Needed because each
 metadata entry corresponds to a recommendation (FK)
----------------------------------------------------------------------------------------------- """
def store_recommendation_and_metadata_to_db(db: Session, sub_id: int, label: str, recommendations: list) -> None:

    for plant in recommendations:
        recommendation_id = store_bm25_recommendation_in_db(db=db,
                                        sub_id=sub_id,
                                        plant_id=plant.id,
                                        label=label)

        store_bm25_metadata_in_db(db=db,
                                  metadata=plant.metadata,
                                  rec_id=recommendation_id)
