from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from starlette import status
from app.database.database import get_db
from app.schemas import Plant
from app.services import plant_service
from app.enums import Growth, Soil, SunLight, Watering, Fertilization

plants_router = APIRouter(prefix="/plants", tags=["Plants"])


""" -----------------------------------------------------------------------------------------------
 Simple endpoint that returns all available plants from the dataset.
----------------------------------------------------------------------------------------------- """
@plants_router.get("/all",
                 summary="Get all Plants",
                 response_model=list[Plant],
                 status_code=status.HTTP_200_OK)

def get_all_plants(skip: int = Query(0, ge=0, description="Number of entries to skip"),
                   limit: int = Query(10, gt=0, le=600, description="Number of entries to return"),
                   db: Session = Depends(get_db)):

    """
    Get all available plants. Pagination possible.
    """

    plants = plant_service.fetch_plants(db=db, skip=skip, limit=limit)
    return plants


""" -----------------------------------------------------------------------------------------------
 Endpoint that allows filtering by given criteria
----------------------------------------------------------------------------------------------- """
@plants_router.get("/filter",
                 summary="Filter Plants",
                 response_model=list[Plant],
                 status_code=status.HTTP_200_OK)

def filter_plants(name: str = Query(None, description="Search for exact or similar names"),
                  growth: Growth = Query(None, description="Filter by growth speed"),
                  soil: Soil = Query(None, description="Filter by soil type"),
                  sun: SunLight = Query(None, description="Filter by sun light"),
                  water: Watering = Query(None, description="Filter by water options"),
                  fertilization: Fertilization = Query(None, description="Filter by fertilization type"),
                  db: Session = Depends(get_db)):

    """
    Filter plants by different options. If no filter option - all plants are returned
    """

    filtered_plants = plant_service.filter_plants(db=db,
                                                  name=name,
                                                  growth=growth,
                                                  soil=soil,
                                                  sun=sun,
                                                  water=water,
                                                  fertilization=fertilization)
    return filtered_plants

