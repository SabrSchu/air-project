from app.schemas.test_schema import TestResponse


""" -----------------------------------------------------------------------------------------------
Basic method that returns a response in the format of the TestResponse schema
----------------------------------------------------------------------------------------------- """
def create_nice_response() -> TestResponse:
    return TestResponse(
        title="Hello Fellow.",
        message="Yay endpoint access works!",
        some_number=444
    )