from sqlalchemy.orm import Session
from app.models import Plant, Answer, Question
from app.schemas import UserAnswerSubmission, Plant as PlantSchema

# user answers water: low, moderate, high, don't care
# water database entries: keep soil consistently moist, keep soil evenly moist, keep soil moist, keep soil
#                   slightly moist, let soil dry between watering, regular watering, "regular, moist soil",
#                   "regular, well-drained soil", water weekly

# user answers sun: full, indirect, partial
# sun database entries: full sunlight, indirect sunlight, partial sunlight

# user answers soil: drained, sandy, moist, loamy, acidic, don't care
# soil db entries: well-drained, sandy, moist, loamy, acidic

# user answers fertilizer: no, yes, don't care
# fertilizer db entries: acidic, low-nitrogen, balanced, no, organic

# user answers growth: fast, moderate, slow, don't care
# growth db entries: slow, moderate, fast






DB_ANSWER_MAPPING_WATER = {
    "keep soil consistently moist": "high",
    "keep soil evenly moist": "high",
    "keep soil moist": "high",
    "keep soil slightly moist": "high",
    "let soil dry between watering": "low",
    "regular watering": "moderate",
    "regular, moist soil": "moderate",
    "regular, well-drained soil": "moderate",
    "water weekly": "low",
    "water when soil feels dry": "low",
    "water when soil is dry": "low",
    "water when topsoil is dry": "low"
}

DB_ANSWER_MAPPING_SUN = {
    "full sunlight": "full",
    "indirect sunlight": "indirect",
    "partial sunlight": "partial"
}

DB_ANSWER_MAPPING_SOIL = {
    "well-drained": "drained",
    "sandy": "sandy",
    "moist": "moist",
    "loamy": "loamy",
    "acidic": "acidic"
}

DB_ANSWER_MAPPING_FERTILIZER = {
    "acidic": "yes",
    "low-nitrogen": "yes",
    "balanced": "yes",
    "organic": "yes",
    "no": "no"
}

DB_ANSWER_MAPPING_GROWTH = {
    "slow": "slow",
    "moderate": "moderate",
    "fast": "fast"
}




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

    # todo process free text

    return clean_preprocessed_user_query


def get_plant_based_on_bm25_document(db: Session, results: list):
    plants = []

    for doc in results:
        plant_id = doc.split(" ")[0]
        plant = db.query(Plant).filter_by(id=plant_id).first()
        plants.append(PlantSchema.model_validate(plant))

    return plants


def get_top_n_good_fits():
    # list of scores
    # find max value
    # divide by 2
    # find first n appearences that have +- threshold of this score
    # get their indices
    # get the elements from corpus
    # find elements in db based on corpus
    pass

def get_top_n_mismatches(db: Session, scores: list, corpus: list):
    # list of scores
    # find first n appearences of 0
    # get their indices
    # get the elements from corpus
    # find elements in db based on corpus
    pass


