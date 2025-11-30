from pydantic import BaseModel, ConfigDict

""" -----------------------------------------------------------------------------------------------
 Schema for returning metadata of a recommendation
----------------------------------------------------------------------------------------------- """
class RecommendationMetadataBM25(BaseModel):
    algorithm: str = "BM25"
    score_raw: float
    score_normalized: float
    score_percentile: float
    rank: int
    matched_terms: list[str]
    unmatched_terms: list[str]
    max_matches: int
    match_count: int
    match_ratio: float


""" -----------------------------------------------------------------------------------------------
 Schema for returning metadata of a recommendation
----------------------------------------------------------------------------------------------- """
class RecommendationMetadataSBERT(BaseModel):
    cosine_sim_raw: float


""" -----------------------------------------------------------------------------------------------
 Schema for response format of plant information
----------------------------------------------------------------------------------------------- """
class Plant(BaseModel):
    id: int
    name: str
    growth: str
    soil: str
    sunlight: str
    watering: str
    fertilization: str
    image_url: str | None

    # needed for transforming db model to schema
    model_config = ConfigDict(from_attributes=True)

""" -----------------------------------------------------------------------------------------------
 Schema for including metadata to the plant recommendation
----------------------------------------------------------------------------------------------- """
class PlantMetadata(Plant):
    metadata: RecommendationMetadataBM25 | RecommendationMetadataSBERT


""" -----------------------------------------------------------------------------------------------
 Schema for returning recommendations based on different labels (perfect fit, good fit, mismatch)
----------------------------------------------------------------------------------------------- """
class PlantRecommendation(BaseModel):
    label: str
    submission_id: int
    recommendation: list[PlantMetadata]

    model_config = ConfigDict(from_attributes=True)
