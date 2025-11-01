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
