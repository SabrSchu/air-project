from enum import Enum

""" -----------------------------------------------------------------------------------------------
 Enums mapping database entries
----------------------------------------------------------------------------------------------- """
class Label(str, Enum):
    perfect = "perfect"
    good = "good"
    mismatch = "mismatch"


class Algorithm(str, Enum):
    bm25 = "bm25"
    sbert = "sbert"