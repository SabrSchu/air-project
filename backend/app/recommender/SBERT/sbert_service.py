from sqlalchemy.orm import Session
from app.models import Plant
from app.schemas import UserFreeTextSubmission


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


def create_text_representation_user_query(user_query: UserFreeTextSubmission) -> str:
    return user_query.free_text
