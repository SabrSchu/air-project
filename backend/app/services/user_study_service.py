import json
from datetime import datetime
from pathlib import Path
from fastapi import HTTPException
from ..schemas import UserStudySubmission


REPORTS_PATH = Path(__file__).parent.parent / "user_study/reports"


""" -----------------------------------------------------------------------------------------------
 Hardcoded validation dictionary, because every other way of input validation is too complex (for me)
----------------------------------------------------------------------------------------------- """
QUESTIONNAIRE_JSON_VALIDATION = {
        1: {
            "items": {
                1: {"type": "scale_1_5", "range": (1, 5)},
                2: {"type": "scale_1_5", "range": (1, 5)},
                3: {"type": "scale_1_5", "range": (1, 5)},
                4: {"type": "scale_1_5", "range": (1, 5)},
            }
        },
        2: {
            "items": {
                1: {"type": "scale_1_5", "range": (1, 5)},
                2: {"type": "scale_1_5", "range": (1, 5)},
                3: {"type": "scale_1_5", "range": (1, 5)},
                4: {"type": "scale_1_5", "range": (1, 5)},
                5: {"type": "scale_1_5", "range": (1, 5)},
                6: {"type": "scale_1_5", "range": (1, 5)},
            }
        },
        3: {
            "items": {
                1: {"type": "scale_1_5", "range": (1, 5)},
                2: {"type": "scale_1_5", "range": (1, 5)},
                3: {"type": "scale_1_5", "range": (1, 5)},
                4: {"type": "scale_1_5", "range": (1, 5)},
                5: {"type": "scale_1_5", "range": (1, 5)},
                6: {"type": "scale_1_5", "range": (1, 5)},
            }
        },
        4: {
            "items": {
                1: {"type": "free_text"},
                2: {"type": "free_text"},
            }
        },
        5: {
            "items": {
                1: {"type": "scale_1_5", "range": (1, 5)}
            }
        }
}


""" -----------------------------------------------------------------------------------------------
 Stores the user study in simple json format in the folder user_study/reports.
----------------------------------------------------------------------------------------------- """
def store_submission(submission: UserStudySubmission):

    # Making the date field to iso format, else exception
    data = submission.model_dump(exclude_none=True)
    if isinstance(data.get("created_at"), datetime):
       data["created_at"] = data["created_at"].isoformat()

    # In case some usernames are identical, counter makes files unique
    num_reports = len(list(REPORTS_PATH.glob("*.json")))
    file_name = f"{submission.user_name}_{num_reports + 1}.json"

    file_path = REPORTS_PATH / file_name

    with file_path.open("w", encoding="utf-8") as user_study_file:
        json.dump(data, user_study_file, indent=2, ensure_ascii=False)


""" -----------------------------------------------------------------------------------------------
 Validates the json that is the user study submission, such that all answers must be correctly
 answered with ratings or free text. It validates the ranges of the scales, and that no
 duplicates are present. The hardcoded dictionary on top is being used for that.
----------------------------------------------------------------------------------------------- """
def validate_submission(submission: UserStudySubmission):
    sections = QUESTIONNAIRE_JSON_VALIDATION.keys()

    grouped_answers = {}
    for item in submission.user_study_answers:
        if item.section_id not in QUESTIONNAIRE_JSON_VALIDATION:
            raise HTTPException(status_code=400, detail=f"Invalid section_id: {item.section_id}")

        grouped_answers.setdefault(item.section_id, {})
        if item.item_id in grouped_answers[item.section_id]:
            raise HTTPException(status_code=400, detail=f"Duplicate item_id: {item.item_id} in section_id: {item.section_id}")

        grouped_answers[item.section_id][item.item_id] = item

    # Now checking for duplicates or missing answers
    if set(grouped_answers.keys()) != set(sections):
        missing = set(sections) - set(grouped_answers.keys())
        extra = set(grouped_answers.keys()) - set(sections)
        raise HTTPException(status_code=400,detail=f"Missing sections: {missing}, duplicates: {extra}")

    # Now validating each answer item individual
    for section_id, spec in QUESTIONNAIRE_JSON_VALIDATION.items():
        expected_items = spec["items"]
        submitted_items = grouped_answers[section_id]

        # Checking for correct item ids
        if set(expected_items.keys()) != set(submitted_items.keys()):
            missing = set(expected_items.keys()) - set(submitted_items.keys())
            extra = set(submitted_items.keys()) - set(expected_items.keys())
            raise HTTPException(status_code=400,detail=f"Section: {section_id}, missing answers: {missing}, extra answer ids: {extra}")

        for item_id, answer_item in expected_items.items():
            item = submitted_items[item_id]

            if answer_item["type"] == "scale_1_5":
                minimum, maximum = answer_item["range"]
                if not (item.rating and minimum <= item.rating <= maximum):
                    raise HTTPException(status_code=400, detail=f"Section: {section_id}, item: {item_id}, rating must be 1 - 5.")
                if item.free_text not in (None, ""):
                    raise HTTPException(status_code=400, detail=f"Section: {section_id}, item: {item_id}, free_text not allowed")

            elif answer_item["type"] == "free_text":
                if item.free_text is None:
                    raise HTTPException(status_code=400,detail=f"Section: {section_id}, item: {item_id}, free_text required")
                if item.rating is not None:
                    raise HTTPException(status_code=400,detail=f"Section: {section_id}, item: {item_id}, rating not allowed")


