from fastapi import APIRouter
from starlette import status
from app.schemas.test_schema import TestResponse
from app.services import test_service


test_router = APIRouter(prefix="", tags=["Test"])


""" -----------------------------------------------------------------------------------------------
A first simple test endpoint that calls a service and returns a nice response pydantic schema
----------------------------------------------------------------------------------------------- """

@test_router.get("/test",
                 summary="Test Router",
                 response_model=TestResponse,
                 status_code=status.HTTP_200_OK)

def test_endpoint():

    """
    Call the test endpoint to see whether your application can access this api.
    """

    test_response = test_service.create_nice_response()

    return test_response