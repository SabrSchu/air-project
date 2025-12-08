from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from starlette import status
from app.database.database import get_db
from app.schemas import DeleteMetadataResponse
from ..schemas.recommendations_schema import RecommendationRatingResponse, AllRecommendations
from ..services import recommendations_service

recommendations_router = APIRouter(prefix="/recommendation", tags=["Recommendations"])


""" -----------------------------------------------------------------------------------------------
 Endpoint that lets the user submit a rating for a entire recommendation
----------------------------------------------------------------------------------------------- """
@recommendations_router.post("/{submission_id}/submit",
                             summary="Rate Recommendation",
                             response_model=RecommendationRatingResponse,
                             status_code=status.HTTP_200_OK)

def rate_recommendation(submission_id: int = Path(description="The submission id of the recommendation received"),
                        rating: int = Query(1, ge=1, le=5, description="Rating number"),
                        db: Session = Depends(get_db)):

    """
    Rate your received recommendation.
    """

    try:
        submission = recommendations_service.add_rating_to_recommendation(db=db, submission_id=submission_id, rating=rating)

        if not submission:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect submission ID!")

        return RecommendationRatingResponse(
            submission_id=submission.id,
            created_at=submission.created_at,
            rating=submission.rating
        )

    except HTTPException:
        raise
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Unexpected error rating recommendation")


""" -----------------------------------------------------------------------------------------------
 Endpoint that lets the user fetch all ever received recommendations. Filter option to include
 or exclude not rated recommendations.
----------------------------------------------------------------------------------------------- """
@recommendations_router.get("/all",
                            summary="Get all  Recommendations",
                            response_model=list[AllRecommendations],
                            status_code=status.HTTP_200_OK)

def get_all_ratings(include_unrated: bool = True,
                    db: Session = Depends(get_db)):

    """
    Get all past received recommendations, decide whether to include unrated recommendations too
    """

    try:
        all_recs = recommendations_service.get_all_recommendations(db=db, include_non_rated=include_unrated)
        return all_recs

    except HTTPException:
        raise
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Unexpected error fetching all received recommendations")


""" -----------------------------------------------------------------------------------------------
 Endpoint that deletes all stored user data about recommendations (user studys stay!) This
 is a helper for development
----------------------------------------------------------------------------------------------- """
@recommendations_router.delete("/metadata",
                               summary="Helper to clear all stored user data",
                               response_model=DeleteMetadataResponse,
                               status_code=status.HTTP_200_OK)

def delete_all_data(db: Session = Depends(get_db)):
    """
    Deletes all stored data (user submissions, recommendations, likes). Handy for testing and Frontend stuff.
    """
    try:
        recommendations_service.delete_all_entries(db=db)
        return DeleteMetadataResponse(
            detail="All data deleted successfully!"
        )

    except HTTPException:
        raise
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Unexpected error deleting stored data")