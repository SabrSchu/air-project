from enum import Enum

""" -----------------------------------------------------------------------------------------------
 Enum mapping database entries
----------------------------------------------------------------------------------------------- """
class Soil(str, Enum):
    well_drained = "well_drained"
    sandy = "sandy"
    moist = "moist"
    loamy = "loamy"
    acidic = "acidic"

    # To have same format for white spaces everywhere
    @property
    def map_db_value(self) -> str:
        mapping = {
            "well_drained": "well-drained",
            "sandy": "sandy",
            "moist":"moist",
            "loamy": "loamy",
            "acidic": "acidic"
        }
        return mapping[self.value]