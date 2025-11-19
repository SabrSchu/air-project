from enum import Enum

""" -----------------------------------------------------------------------------------------------
 Enum mapping database entries
----------------------------------------------------------------------------------------------- """
class Watering(str, Enum):
    consistently_moist = "consistently_moist"
    evenly_moist = "evenly_moist"
    moist = "moist"
    regular_moist = "regular_moist"
    regular = "regular"
    slightly_moist = "slightly_moist"
    regular_well_drained = "regular_well_drained"
    water_when_dry = "water_when_dry"
    weekly = "weekly"

    # Mapping to avoid whitespace in query
    @property
    def map_db_value(self) -> list[str]:
        mapping = {
            "consistently_moist": ["keep soil consistently moist"],
            "evenly_moist": ["keep soil evenly moist"],
            "moist": ["keep soil moist"],
            "slightly_moist": ["keep soil slightly moist"],
            "water_when_dry": ["let soil dry between watering", "water when soil feels dry",
                               "water when soil is dry", "water when topsoil is dry"],
            "regular": ["regular watering"],
            "regular_moist": ["regular, moist soil"],
            "regular_well_drained": ["regular, well-drained soil"],
            "weekly": ["water weekly"]
        }
        return mapping[self.value]