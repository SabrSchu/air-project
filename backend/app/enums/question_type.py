from enum import Enum

""" -----------------------------------------------------------------------------------------------
 Enum mapping database entries
----------------------------------------------------------------------------------------------- """
class QuestionType(str, Enum):
    water = "water"
    sun = "sun"
    soil = "soil"
    fertilizer = "fertilizer"
    growth = "growth"


class UserStudyAnswerType(str, Enum):
    rating = "rating"
    free_text = "free_text"