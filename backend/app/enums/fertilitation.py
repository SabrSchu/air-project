from enum import Enum

""" -----------------------------------------------------------------------------------------------
 Enum mapping database entries
----------------------------------------------------------------------------------------------- """
class Fertilization(str, Enum):
    acidic = "acidic"
    low_nitrogen = "low_nitrogen"
    balanced = "balanced"
    no = "no"
    organic = "organic"

    # Mapping to avoid whitespace in query
    @property
    def map_db_value(self) -> str:
        mapping = {
            "acidic": "acidic",
            "low_nitrogen": "low-nitrogen",
            "balanced": "balanced",
            "no": "no",
            "organic": "organic",
        }
        return mapping[self.value]