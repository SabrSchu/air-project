from pydantic import BaseModel


""" -----------------------------------------------------------------------------------------------
 Schema for response format of plant information
----------------------------------------------------------------------------------------------- """
class Plant(BaseModel):
    name: str
    growth: str
    soil: str
    sunlight: str
    watering: str
    fertilization: str