from sqlalchemy.orm import Session
from app.models import Plant
from app.schemas import UserFreeTextSubmission


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
def get_plant_data_from_score_indices(db: Session, indices: list, scores: list, num: int) -> list[Plant]:
    #print("\n\n plant Indices in function: ", indices)
    #print("Scores:                      ", scores)

    plant_results: list = []
    plants_with_image_url: list = []
    plants_without_image_url: list = []

    for plant_idx in indices:
        plant = db.query(Plant).filter_by(id=plant_idx + 1).first()

        if plant and plant.image_url != "":
            plants_with_image_url.append(plant)
        elif plant:
            plants_without_image_url.append(plant)

    plant_results = plants_with_image_url + plants_without_image_url

    return plant_results[:num]


""" -----------------------------------------------------------------------------------------------
 Helper printing results.
----------------------------------------------------------------------------------------------- """
def print_infos(plants: list[Plant], title: str):

    print(f"----- {title} match -----")
    for i, plant in enumerate(plants):
        print(f"Plant ID: {plant.id}, name:{plant.name}")

