from fastapi import APIRouter, Query
from starlette import status
from app.schemas import Plant
from app.services import plant_service

plants_router = APIRouter(prefix="/plants", tags=["Plants"])


""" -----------------------------------------------------------------------------------------------
 Simple endpoint that returns all available plants from the dataset.
----------------------------------------------------------------------------------------------- """
@plants_router.get("/all",
                 summary="Get all Plants",
                 response_model=list[Plant],
                 status_code=status.HTTP_200_OK)

def get_all_plants(skip: int = Query(0, ge=0, description="Number of entries to skip"),
                   limit: int = Query(10, gt=0, le=600, description="Number of entries to return")):

    """
    Get all available plants. Pagination possible.
    """

    plant_df = plant_service.get_dataset()
    plants_data = plant_df.to_dict(orient="records")

    paginated_plant_list = plants_data[skip : skip + limit]

    return paginated_plant_list


""" -----------------------------------------------------------------------------------------------
 Endpoint that allows filtering by given criteria
----------------------------------------------------------------------------------------------- """
@plants_router.get("/filter",
                 summary="Filter Plants",
                 response_model=list[Plant],
                 status_code=status.HTTP_200_OK)

def filter_plants(skip: int = Query(0, ge=0, description="Number of entries to skip"),
                   limit: int = Query(10, gt=0, le=600, description="Number of entries to return")):

    """
    Filter plants. Pagination possible.
    """

    plant_df = plant_service.get_dataset()

    #todo

