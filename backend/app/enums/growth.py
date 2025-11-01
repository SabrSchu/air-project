from enum import Enum

""" -----------------------------------------------------------------------------------------------
 Enum mapping database entries
----------------------------------------------------------------------------------------------- """
class Growth(str, Enum):
    slow = "slow"
    moderate = "moderate"
    fast = "fast"