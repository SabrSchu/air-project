""" -----------------------------------------------------------------------------------------------
 Mappings for processing database entries and user answers. This is necessary for further steps
 in using BM25 recommender.
----------------------------------------------------------------------------------------------- """
DB_ANSWER_MAPPING_WATER = {
    "keep soil consistently moist": "high",
    "keep soil evenly moist": "high",
    "keep soil moist": "high",
    "keep soil slightly moist": "high",
    "let soil dry between watering": "low",
    "regular watering": "moderate",
    "regular, moist soil": "moderate",
    "regular, well-drained soil": "moderate",
    "water weekly": "low",
    "water when soil feels dry": "low",
    "water when soil is dry": "low",
    "water when topsoil is dry": "low"
}

DB_ANSWER_MAPPING_SUN = {
    "full sunlight": "full",
    "indirect sunlight": "indirect",
    "partial sunlight": "partial"
}

DB_ANSWER_MAPPING_SOIL = {
    "well-drained": "drained",
    "sandy": "sandy",
    "moist": "moist",
    "loamy": "loamy",
    "acidic": "acidic"
}

DB_ANSWER_MAPPING_FERTILIZER = {
    "acidic": "yes",
    "low-nitrogen": "yes",
    "balanced": "yes",
    "organic": "yes",
    "no": "no"
}

DB_ANSWER_MAPPING_GROWTH = {
    "slow": "slow",
    "moderate": "moderate",
    "fast": "fast"
}