import pandas as pd
from pathlib import Path
from pandas import DataFrame

DATASET_PATH = Path(__file__).parent.parent / "dataset/plants_clean.csv"

""" -----------------------------------------------------------------------------------------------
 Helper that reads dataset into dataframe and transforms column names to schema
----------------------------------------------------------------------------------------------- """
def get_dataset() -> DataFrame:
    df = pd.read_csv(DATASET_PATH)

    df = df.rename(columns={
        "Plant Name": "name",
        "Growth": "growth",
        "Soil": "soil",
        "Sunlight": "sunlight",
        "Watering": "watering",
        "Fertilization Type": "fertilization"
    })

    return df