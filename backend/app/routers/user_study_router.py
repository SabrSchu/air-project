import json
from pathlib import Path
from fastapi import APIRouter, HTTPException
from starlette import status
from ..schemas import UserStudySubmission, UserStudySubmitted
from ..services import user_study_service

user_study_router = APIRouter(prefix="/user_study", tags=["User Study"])

QUESTIONNAIRE_PATH = Path(__file__).parent.parent / "user_study/user_study_questions.json"
FINISHED_USER_STUDIES_PATH = Path(__file__).parent.parent / "user_study/reports"


""" -----------------------------------------------------------------------------------------------
 Endpoint that returns the user study questionnaire for the frontend to display
----------------------------------------------------------------------------------------------- """
@user_study_router.get("/questions",
                 summary="Get all User Study questions with answer options",
                 status_code=status.HTTP_200_OK)

def get_user_study_questionnaire():

    """
    Get available user study questions with answer options.
    """
    try:

        with QUESTIONNAIRE_PATH.open("r", encoding="utf-8") as f:
            user_study_questions = json.load(f)

        return user_study_questions

    except HTTPException:
        raise
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Unexpected error retrieving user study questionnaire!")


""" -----------------------------------------------------------------------------------------------
 Endpoint that lets the user submit the user study in the end.
----------------------------------------------------------------------------------------------- """
@user_study_router.post("/submit",
                        summary="Submit your User Study!",
                        response_model=UserStudySubmitted,
                        status_code=status.HTTP_201_CREATED)

def submit_user_study(submission: UserStudySubmission):
    """
    Submit the user study answers! They will be stored locally.
    """
    try:

        user_study_service.validate_submission(submission=submission)

        user_study_service.store_submission(submission=submission)

        return UserStudySubmitted(detail="User Study submitted successfully!")

    except HTTPException:
        raise
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Unexpected error submitting user study!")


""" -----------------------------------------------------------------------------------------------
 Endpoint that returns all ever posted user studies. For further processing or evaluation.
----------------------------------------------------------------------------------------------- """
@user_study_router.get("/all",
                 summary="Get all submitted user studies",
                 status_code=status.HTTP_200_OK)

def get_user_study_questionnaire():

    """
    Get all user studies that were submitted, as a list of json files.
    """
    try:
        user_studies = []

        for file_path in FINISHED_USER_STUDIES_PATH.glob("*.json"):
            with file_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
                user_studies.append(data)

        return user_studies

    except HTTPException:
        raise
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Unexpected error retrieving user studies!")



