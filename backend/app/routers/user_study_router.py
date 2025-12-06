import json
from pathlib import Path
from fastapi import APIRouter, Depends
from starlette import status



user_study_router = APIRouter(prefix="/user_study", tags=["User Study"])

QUESTIONNAIRE_PATH = Path(__file__).parent.parent / "user_study/user_study_questions.json"

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

    with QUESTIONNAIRE_PATH.open("r", encoding="utf-8") as f:
        user_study_questions = json.load(f)

    return user_study_questions



