from pydantic import BaseModel

""" -----------------------------------------------------------------------------------------------
Simple pydantic schema, where we can determine the request/response formats and input validation
----------------------------------------------------------------------------------------------- """
class TestResponse(BaseModel):
    title: str
    message: str
    some_number: int