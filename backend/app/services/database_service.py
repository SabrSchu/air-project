import csv
from pathlib import Path
from sqlalchemy.orm import Session

from ..enums import QuestionType
from ..models import Plant, Question, Answer

FILE_PATH = Path(__file__).parent.parent / "dataset/plants_enriched.csv"


""" -----------------------------------------------------------------------------------------------
 Upon startup, once the csv is loaded to the database, if database is empty, else nothing todo.
----------------------------------------------------------------------------------------------- """
def store_csv_entries_to_db(db: Session):

    # Only store entries if table is empty
    if db.query(Plant).first():
        return

    with open(FILE_PATH, 'r', encoding='utf-8') as plant_dataset:
        reader = csv.DictReader(plant_dataset)
        plants = []
        for row in reader:
            plant = Plant(
                name=row["plant name"],
                growth=row["growth"],
                soil=row["soil"],
                sunlight=row["sunlight"],
                watering=row["watering"],
                fertilization=row["fertilization type"],
                image_url=row["image_url"]
            )
            plants.append(plant)

        db.add_all(plants)
        db.commit()


""" -----------------------------------------------------------------------------------------------
 Upon startup, once the available quiz questions are stored to the database, if it is empty.
 Hardcoded entries are neither elegant nor a good solution, but sufficient for this task
----------------------------------------------------------------------------------------------- """
def store_questions_to_db(db: Session):

    # Only store entries when table is empty
    if db.query(Question).first():
        return

    questions = [
        {
            "type": QuestionType.water,
            "question": "How much time do you want to spend on watering the plant?"
        },
        {
            "type": QuestionType.sun,
            "question": "How much sunlight does the plant's spot get?"
        },
        {
            "type": QuestionType.soil,
            "question": "What soil type do you prefer?"
        },
        {
            "type": QuestionType.fertilizer,
            "question": "Is it ok for you to use a fertilizer regularly?"
        },
        {
            "type": QuestionType.growth,
            "question": "Do you want something that grows quickly or stays small?"
        }
    ]

    for question in questions:
        db.add(Question(type=question["type"], question=question["question"]))

    db.commit()


""" -----------------------------------------------------------------------------------------------
 Upon startup, once the available quiz answer options are stored to the database, if it is empty.
 Hardcoded entries are neither elegant nor a good solution, but sufficient for this task
----------------------------------------------------------------------------------------------- """
def store_answer_options_to_db(db: Session):

    # Only store entries when table is empty
    if db.query(Answer).first():
        return

    answer_options = [
        {
            "type": QuestionType.water,
            "answer": "low",
            "question_id": 1
        },
        {
            "type": QuestionType.water,
            "answer": "moderate",
            "question_id": 1
        },
        {
            "type": QuestionType.water,
            "answer": "high",
            "question_id": 1
        },
        {
            "type": QuestionType.water,
            "answer": "don't care",
            "question_id": 1
        },
        {
            "type": QuestionType.sun,
            "answer": "full",
            "question_id": 2
        },
        {
            "type": QuestionType.sun,
            "answer": "indirect",
            "question_id": 2
        },
        {
            "type": QuestionType.sun,
            "answer": "partial",
            "question_id": 2
        },
        {
            "type": QuestionType.soil,
            "answer": "drained",
            "question_id": 3
        },
        {
            "type": QuestionType.soil,
            "answer": "sandy",
            "question_id": 3
        },
        {
            "type": QuestionType.soil,
            "answer": "moist",
            "question_id": 3
        },
        {
            "type": QuestionType.soil,
            "answer": "loamy",
            "question_id": 3
        },
        {
            "type": QuestionType.soil,
            "answer": "acidic",
            "question_id": 3
        },
        {
            "type": QuestionType.soil,
            "answer": "dont' care",
            "question_id": 3
        },
        {
            "type": QuestionType.fertilizer,
            "answer": "no",
            "question_id": 4
        },
        {
            "type": QuestionType.fertilizer,
            "answer": "yes",
            "question_id": 4
        },
        {
            "type": QuestionType.fertilizer,
            "answer": "don't care",
            "question_id": 4
        },
        {
            "type": QuestionType.growth,
            "answer": "fast",
            "question_id": 5
        },
        {
            "type": QuestionType.growth,
            "answer": "moderate",
            "question_id": 5
        },
        {
            "type": QuestionType.growth,
            "answer": "slow",
            "question_id": 5
        },
        {
            "type": QuestionType.growth,
            "answer": "don't care",
            "question_id": 5
        }
    ]

    for answer in answer_options:
        db.add(Answer(type=answer["type"], answer=answer["answer"], question_id=answer["question_id"]))

    db.commit()
