import pandas as pd
from pathlib import Path
from app.schemas import DataSetHeaders

DATASET_PATH = Path(__file__).parent.parent / "dataset/plant_dataset_raw.csv"

""" -----------------------------------------------------------------------------------------------
Helper method that interacts with the dataset. Todo: Maybe extract this functionality into a 
separate class, and then this service just calls the real data-process class.
----------------------------------------------------------------------------------------------- """

def get_dataset_headers() -> DataSetHeaders:
    dataframe = pd.read_csv(DATASET_PATH, nrows=0)
    columns = dataframe.columns.tolist()

    return DataSetHeaders(headers=columns)