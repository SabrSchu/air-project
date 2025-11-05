from pydantic import BaseModel, ConfigDict

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
 Schema for returning recommendations based on different labels (perfect fit, good fit, mismatch)
----------------------------------------------------------------------------------------------- """
class PlantRecommendation(BaseModel):
    label: str
    recommendation: list[Plant]

    model_config = ConfigDict(from_attributes=True)
