import random
import numpy as np
from sqlalchemy.orm import Session
from app.models import Plant, Answer, Question
from app.schemas import UserAnswerSubmission, Plant as PlantSchema
from .bm25_mappings import DB_ANSWER_MAPPING_GROWTH, DB_ANSWER_MAPPING_WATER, DB_ANSWER_MAPPING_SOIL, \
                      DB_ANSWER_MAPPING_SUN, DB_ANSWER_MAPPING_FERTILIZER



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
            str(plant.name),
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
 the documents, and searches for the plants based on this id in the db. 
 Returns list of Plants, which are the base for a Plant recommendation. Plant entries with image
 url are preferred.
----------------------------------------------------------------------------------------------- """
def get_plant_based_on_bm25_document(db: Session, results: list, max_results: int) -> list[Plant]:
    plants: list = []
    plants_with_img: list = []
    plants_without_img: list = []

    for doc in results:
        plant_id = doc.split(" ")[0]
        plant = db.query(Plant).filter_by(id=plant_id).first()
        plants.append(PlantSchema.model_validate(plant))

        if plant and plant.image_url != "":
            plants_with_img.append(PlantSchema.model_validate(plant))
        elif plant:
            plants_without_img.append(PlantSchema.model_validate(plant))

        if len(plants_with_img) == max_results:
            break

    plants = plants_with_img + plants_without_img

    return plants[:max_results]


""" -----------------------------------------------------------------------------------------------
 Additionally to finding "perfect fits" we also want to return "moderate good fits" and "mismatches".
 For that we take the scores returned by the BM25 (each score corresponds to a plant entry in the
 corpus), and manually choose the percentile of the fit we want to get. Mismatches are in the lowest
 percentiles, moderate/good fits we search in the 70th-90th percentile.
----------------------------------------------------------------------------------------------- """
def get_fits_in_percentile(scores: list, dataset_corpus: list, n: int, min_p: int, max_p: int) -> list:
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
    good_fits: list = []
    for element in random_n:
        good_fits.append(dataset_corpus[element])

    return good_fits



