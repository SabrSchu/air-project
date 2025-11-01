from enum import Enum

""" -----------------------------------------------------------------------------------------------
 Enum mapping database entries
----------------------------------------------------------------------------------------------- """
class SunLight(str, Enum):
    full_sunlight = "full_sunlight"
    indirect_light = "indirect_sunlight"
    partial_light = "partial_sunlight"

    # Mapping to avoid whitespace in query
    @property
    def map_db_value(self) -> str:
        mapping = {
            "full_sunlight": "full sunlight",
            "indirect_sunlight": "indirect sunlight",
            "partial_sunlight": "partial sunlight"
        }
        return mapping[self.value]