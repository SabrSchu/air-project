from pydantic import BaseModel

""" -----------------------------------------------------------------------------------------------
Simple pydantic schema, where we can determine the request/response formats and input validation
----------------------------------------------------------------------------------------------- """
class DataSetHeaders(BaseModel):
    headers: list[str]
