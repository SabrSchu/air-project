import csv
from pathlib import Path
from sqlalchemy.orm import Session
from ..models import Plant

FILE_PATH = Path(__file__).parent.parent / "dataset/plants_enriched.csv"


""" -----------------------------------------------------------------------------------------------
 Upon startup, once the csv is loaded to the database, if database is empty, else nothing todo.
----------------------------------------------------------------------------------------------- """
def store_csv_entries_to_db(db: Session):

    # Only store entries if table is empty
    if db.query(Plant).first():
        return

    with open(FILE_PATH, 'r', encoding='utf-8') as plant_dataset:
        reader = csv.DictReader(plant_dataset)
        plants = []
        for row in reader:
            plant = Plant(
                name=row["plant name"],
                growth=row["growth"],
                soil=row["soil"],
                sunlight=row["sunlight"],
                watering=row["watering"],
                fertilization=row["fertilization type"],
                image_url=row["image_url"]
            )
            plants.append(plant)

        db.add_all(plants)
        db.commit()