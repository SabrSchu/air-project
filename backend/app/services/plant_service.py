from pathlib import Path
from typing import Optional
from sqlalchemy.orm import Session, Query
from app.enums import Growth, Soil, SunLight, Watering, Fertilization
from app.models import Plant, UserPlantLike
from app.schemas import PlantLikeResponse


DATASET_PATH = Path(__file__).parent.parent / "dataset/plants_clean.csv"


""" -----------------------------------------------------------------------------------------------
 Query all plants including pagination
----------------------------------------------------------------------------------------------- """
def fetch_plants(db: Session, skip: int, limit: int) -> list[type[Plant]]:
    return db.query(Plant).offset(skip).limit(limit).all()


""" -----------------------------------------------------------------------------------------------
 Query plant via id
----------------------------------------------------------------------------------------------- """
def get_plant_by_id(db: Session, plant_id: int) -> Optional[Plant]:
    return db.query(Plant).filter_by(id=plant_id).first()


""" -----------------------------------------------------------------------------------------------
 Get like count
----------------------------------------------------------------------------------------------- """
def get_plant_likes(db: Session, plant_id: int) -> int:
    like_entry = db.query(UserPlantLike).filter_by(plant_id=plant_id).first()
    return like_entry.like_counter


""" -----------------------------------------------------------------------------------------------
 Get a list of all liked plants of the user
----------------------------------------------------------------------------------------------- """
def get_all_liked_plants(db: Session) -> Optional[list[PlantLikeResponse]]:
    all_like_entries = db.query(UserPlantLike).all()

    all_liked_plants: list = []
    for entry in all_like_entries:

        plant = get_plant_by_id(db=db, plant_id=entry.plant_id) # type: ignore

        all_liked_plants.append(
            PlantLikeResponse(
                id=plant.id,
                name=plant.name,
                growth=plant.growth,
                soil=plant.soil,
                sunlight=plant.sunlight,
                watering=plant.watering,
                fertilization=plant.fertilization,
                image_url=plant.image_url,
                like_counter=entry.like_counter # type: ignore
            )
        )

    return all_liked_plants


""" -----------------------------------------------------------------------------------------------
 Add a like to a plant
----------------------------------------------------------------------------------------------- """
def add_like(db: Session, plant_id: int) -> int:
    like_entry = db.query(UserPlantLike).filter_by(plant_id=plant_id).first()

    if not like_entry:
        like_entry = UserPlantLike(plant_id=plant_id, like_counter=1)
        db.add(like_entry)
    else:
        like_entry.like_counter += 1

    db.commit()
    db.refresh(like_entry)
    return like_entry.like_counter


""" -----------------------------------------------------------------------------------------------
 Query all plants with filter params
----------------------------------------------------------------------------------------------- """
def filter_plants(db: Session,
                  name: str | None = None,
                  growth: Growth | None = None,
                  soil: Soil | None = None,
                  sun: SunLight | None = None,
                  water: Watering | None = None,
                  fertilization: Fertilization | None = None
                  ) -> Query[type[Plant]]:
    found_plants = db.query(Plant)

    if name:
        found_plants = found_plants.filter(Plant.name.ilike(f"%{name}%"))

    if growth:
        found_plants = found_plants.filter(Plant.growth == growth.value)

    if soil:
        found_plants = found_plants.filter(Plant.soil == soil.map_db_value)

    if sun:
        found_plants = found_plants.filter(Plant.sunlight == sun.map_db_value)

    if water:
        db_values = water.map_db_value
        found_plants = found_plants.filter(Plant.watering.in_(db_values))

    if fertilization:
        found_plants = found_plants.filter(Plant.fertilization == fertilization.map_db_value)

    return found_plants


