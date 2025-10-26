import pandas as pd
from pathlib import Path

DATASET_PATH_RAW = Path(__file__).parent.parent / "dataset/plants_raw.csv"
DATASET_PATH_CLEAN = Path(__file__).parent.parent / "dataset/plants_clean.csv"


""" -----------------------------------------------------------------------------------------------
 The chosen dataset is clean, without missing fields or incorrect formats. To be sure
 duplicate entries are being deleted, and trailing whitespaces in case there are any.
----------------------------------------------------------------------------------------------- """
def preprocess_dataset():
    lines_clean: list[str] = []

    with open(DATASET_PATH_RAW, "r", encoding="utf-8", errors="replace") as file:
        lines_raw = file.readlines()

    # for each line, remove trailing commas, whitespaces or too many quotes
    for line_raw in lines_raw:

        line_clean = line_raw.replace('"""', '"')
        line_clean = line_clean.rstrip()

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
def print_infos():
    df = pd.read_csv(DATASET_PATH_CLEAN)
    df.info()
    df.describe()



def main():
    preprocess_dataset()
    get_rid_of_duplicates()
    print_infos()


if __name__ == "__main__":
    main()
