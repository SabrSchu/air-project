from pydantic import BaseModel


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


""" -----------------------------------------------------------------------------------------------
 Schema for returning recommendations based on different labels (perfect fit, good fit, mismatch)
----------------------------------------------------------------------------------------------- """
class PlantRecommendation(BaseModel):
    label: str
    recommendation: list[Plant]