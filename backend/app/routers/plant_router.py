from fastapi import APIRouter, Query, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from starlette import status
from starlette.status import HTTP_404_NOT_FOUND

from app.database.database import get_db
from app.schemas import Plant, PlantLikeResponse
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


""" -----------------------------------------------------------------------------------------------
 Endpoint that lets the user store likes to a plant
----------------------------------------------------------------------------------------------- """
@plants_router.post("/{plant_id}/like",
                    summary="Give a like to a single plant",
                    response_model=PlantLikeResponse,
                    status_code=status.HTTP_201_CREATED)

def like_plant(plant_id: int = Path(description="The id of a plant"),
               db: Session = Depends(get_db)):

    """
    Give a like to a plant via plant id.
    """
    try:
        plant = plant_service.get_plant_by_id(db=db, plant_id=plant_id)

        if plant is None:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Plant not found!")

        like_count = plant_service.add_like(db=db, plant_id=plant_id)

        return PlantLikeResponse(
            id = plant.id,
            name=plant.name,
            growth=plant.growth,
            soil=plant.soil,
            sunlight=plant.sunlight,
            watering=plant.watering,
            fertilization=plant.fertilization,
            image_url=plant.image_url,
            like_counter=like_count
        )

    except HTTPException:
        raise
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error liking plant")


""" -----------------------------------------------------------------------------------------------
 Endpoint that returns all liked plants and their like count
----------------------------------------------------------------------------------------------- """
@plants_router.get("/all/likes",
                   summary="Get all liked plants",
                   response_model=list[PlantLikeResponse],
                   status_code=status.HTTP_200_OK)

def get_all_liked_plants(db: Session = Depends(get_db)):

    """
    Get all liked plants of the user
    """
    try:
        all_liked_plants = plant_service.get_all_liked_plants(db=db)
        return all_liked_plants

    except HTTPException:
        raise
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Unexpected error fetching liked plants")