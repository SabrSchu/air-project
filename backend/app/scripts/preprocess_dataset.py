import pandas as pd
from pathlib import Path
from pandas import DataFrame

DATASET_PATH_RAW = Path(__file__).parent.parent / "dataset/plant_dataset_raw.csv"
DATASET_PATH_CLEAN = Path(__file__).parent.parent / "dataset/plant_dataset_clean.csv"


""" -----------------------------------------------------------------------------------------------
 Some lines have a ',' within the string text, and this leads to incorrectly adding a 10th unknown
 column. This method wraps these strings into "" for correct parsing.
----------------------------------------------------------------------------------------------- """
def manually_handle_commas(parts: list) -> str:
    parts = parts[:8] + [','.join(parts[8:])]
    if ',' in parts[8] and not (parts[8].startswith('"') and parts[8].endswith('"')):
        parts[8] = f'"{parts[8]}"'
    line = ",".join(parts)
    return line


""" -----------------------------------------------------------------------------------------------
 Preprocesses the dataset: Removing trailing whitespaces, commas, incorrect formatting.
 Writes the result into new clean csv file.
----------------------------------------------------------------------------------------------- """
def preprocess_dataset():
    lines_clean: list[str] = []

    with open(DATASET_PATH_RAW, "r") as file:
        lines_raw = file.readlines()

    # for each line, remove trailing commas, whitespaces or too many quotes
    for line_raw in lines_raw:

        line_clean = line_raw.replace('"""', '"')
        line_clean = line_clean.rstrip()
        line_clean = line_clean.rstrip(',')

        # handling incorrect formatted commas
        parts = line_clean.split(',')
        if len(parts) > 9:
            line_clean = manually_handle_commas(parts)

        lines_clean.append(line_clean + '\n')

    with open(DATASET_PATH_CLEAN, "w") as file_clean:
        file_clean.writelines(lines_clean)


""" -----------------------------------------------------------------------------------------------
 Some lines have duplicates, built in pandas function handles this.
----------------------------------------------------------------------------------------------- """
def get_rid_of_duplicates():
    df = pd.read_csv(DATASET_PATH_CLEAN)
    df = df.drop_duplicates()
    df.to_csv(DATASET_PATH_CLEAN, index=False)


""" -----------------------------------------------------------------------------------------------
 Small helper for getting an overview over the data
----------------------------------------------------------------------------------------------- """
def print_infos(df: DataFrame):
    df.info()
    df.describe()



def main():
    preprocess_dataset()
    get_rid_of_duplicates()

    df = pd.read_csv(DATASET_PATH_CLEAN)
    print_infos(df)



if __name__ == "__main__":
    main()