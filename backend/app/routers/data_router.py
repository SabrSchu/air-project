from fastapi import APIRouter
from starlette import status
from app.schemas import DataSetHeaders
from app.services import data_service

data_router = APIRouter(prefix="/data", tags=["Data"])


""" -----------------------------------------------------------------------------------------------
A first endpoint that interacts with the dataset. Simple test endpoint that returns all available 
header colum names.
----------------------------------------------------------------------------------------------- """

@data_router.get("/columns",
                 summary="Dataset Router",
                 response_model=DataSetHeaders,
                 status_code=status.HTTP_200_OK)

def test_endpoint():

    """
    Call the test endpoint to get all available headers from the current dataset.
    """

    headers = data_service.get_dataset_headers()

    return headers