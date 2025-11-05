from sqlalchemy import func
from sqlalchemy.orm import Session
from ..models import Plant
from ..schemas import Plant as PlantSchema

""" -----------------------------------------------------------------------------------------------
 Helper method for the placeholder recommender algorithm, fetches random plants from db. Will
 be deleted later
----------------------------------------------------------------------------------------------- """
def fetch_plant_recommendations_randomly(num_plants: int, db: Session) -> list[Plant]:
    random_plants = db.query(Plant).order_by(func.random()).limit(num_plants).all()

    return [PlantSchema.model_validate(plant) for plant in random_plants]
