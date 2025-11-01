from pathlib import Path
from sqlalchemy.orm import Session, Query
from app.enums import Growth, Soil, SunLight, Watering, Fertilization
from app.models import Plant


DATASET_PATH = Path(__file__).parent.parent / "dataset/plants_clean.csv"


""" -----------------------------------------------------------------------------------------------
 Query all plants including pagination
----------------------------------------------------------------------------------------------- """
def fetch_plants(db: Session, skip: int, limit: int) -> list[type[Plant]]:
    return db.query(Plant).offset(skip).limit(limit).all()


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
        found_plants = found_plants.filter(Plant.watering == water.map_db_value)

    if fertilization:
        found_plants = found_plants.filter(Plant.fertilization == fertilization.map_db_value)

    return found_plants


