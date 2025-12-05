from sqlalchemy.orm import Session
from app.models import Plant
from app.schemas import UserFreeTextSubmission, PlantMetadata, RecommendationMetadataSBERT, Plant as PlantSchema

""" -----------------------------------------------------------------------------------------------
 Helper that creates a text representation similar to natural language, out of the existing
 dataset. This is a preprocessing step for the embeddings creation.
----------------------------------------------------------------------------------------------- """
def create_text_representation_plants(db: Session) -> list[tuple[int, str]]:

    all_plants = db.query(Plant).all()

    plant_text_repr: list = []
    for plant in all_plants:
        plant_text_repr.append(
            (plant.id,
            f"{plant.name} that grows {plant.growth}, has {plant.soil} soil, needs {plant.sunlight}, needs "
            f"{plant.fertilization} fertilizer and {plant.watering}.")
        )

    return plant_text_repr


""" -----------------------------------------------------------------------------------------------
 Helper that transforms the user input into a plain string for further processing.
----------------------------------------------------------------------------------------------- """
def create_text_representation_user_query(user_query: UserFreeTextSubmission) -> str:
    return user_query.free_text


""" -----------------------------------------------------------------------------------------------
 Takes the indices of the relevant similarity scores, and searches the database for the 
 corresponding plants. A padding is added to get more results than requested, to be able to 
 prioritize plants that have a image url present.
----------------------------------------------------------------------------------------------- """
def get_plant_data_from_score_indices(db: Session, top_indices: list, top_scores: list, num: int, scores_rank: dict) -> list[PlantMetadata]:

    all_recommendations: list = []
    final_recommendations: list = []

    all_scores = list(scores_rank.keys())
    best_score = max(scores_rank.keys())

    for plant_idx, score in zip(top_indices, top_scores):
        plant_id = plant_idx + 1

        plant = db.query(Plant).filter_by(id=plant_id).first()

        if plant is None:
            continue

        plant_schema = PlantSchema.model_validate(plant)

        # Calculate the metadata stuff
        plant_rank = scores_rank[score]
        normalized_score = calculate_min_max_normalization(all_scores=all_scores, score=score)
        percentile_score = get_score_percentile(all_scores=all_scores, score=score)

        metadata = RecommendationMetadataSBERT(
            algorithm="SBERT",
            cosine_sim_raw=round(score, 4),
            cosine_sim_normalized=normalized_score,
            rank=plant_rank,
            cosine_sim_percentile=round(percentile_score, 2),
            cosine_distance=round(1 - score, 4),
            gap_to_best=round(best_score - score, 4)
        )

        plant_with_metadata = PlantMetadata(
            **plant_schema.model_dump(),
            metadata=metadata
        )

        has_image = bool(plant.image_url) and plant.image_url != ""
        all_recommendations.append((plant_with_metadata, has_image))

        # Preferring those plants with image present
        all_recommendations.sort(key=lambda x: not x[1])
        final_recommendations = [recom for (recom, has_image) in all_recommendations[:num]]

    #todo store to db

    return final_recommendations


""" -----------------------------------------------------------------------------------------------
 Helper that maps scores to rank positions.
----------------------------------------------------------------------------------------------- """
def map_scores_to_rank(all_scores: list[float]) -> dict[float, int]:
    sorted_unique = sorted(set(all_scores), reverse=True)
    rank_and_score = {score: rank for rank, score in enumerate(sorted_unique, start=1)}

    return rank_and_score


""" -----------------------------------------------------------------------------------------------
 Normalizes the raw score for easier comparison. Method Min-Max normalization oriented on:
 https://www.codecademy.com/article/min-max-zscore-normalization (same method as for BM25)
----------------------------------------------------------------------------------------------- """
def calculate_min_max_normalization(all_scores: list, score: float) -> float:
    minimum = min(all_scores)
    maximum = max(all_scores)

    normalized_score = (score - minimum) / (maximum - minimum)

    return round(normalized_score, 2)


""" -----------------------------------------------------------------------------------------------
 Calculates the percentile position of the score. Eg. if the percentile rank of the current score
 is 0.6, this means that the current score is higher than 60% of all scores in the list.
 (Same method as for BM25)
----------------------------------------------------------------------------------------------- """
def get_score_percentile(all_scores: list, score: float) -> float:

    num_scores_below_target = sum(1 for s in all_scores if s < score)
    percentile_rank = (num_scores_below_target / len(all_scores))

    return round(percentile_rank, 3)

