import os
import httpx
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from pandas import DataFrame

DATASET_PATH_RAW = Path(__file__).parent.parent / "dataset/raw/plants_raw.csv"
DATASET_PATH_CLEAN = Path(__file__).parent.parent / "dataset/raw/plants_clean.csv"
DATASET_PATH_ENRICHED = Path(__file__).parent.parent / "dataset/plants_enriched.csv"
DATASET_PATH_FINAL = Path(__file__).parent.parent / "dataset/plants.csv"

PLANT_API_BASE_URL_TREFLE = "https://trefle.io/api/v1/plants"
WIKIPEDIA_BASE_URL = "https://en.wikipedia.org/w/api.php"


""" -----------------------------------------------------------------------------------------------
 The chosen dataset is clean, without missing fields or incorrect formats. To be sure
 duplicate entries are being deleted, and trailing whitespaces in case there are any.
----------------------------------------------------------------------------------------------- """
def preprocess_dataset():
    lines_clean: list[str] = []

    with open(DATASET_PATH_RAW, "r", encoding="utf-8", errors="replace") as file:
        lines_raw = file.readlines()

    for line_raw in lines_raw:

        line_clean = line_raw.replace('"""', '"')
        line_clean = line_clean.rstrip()
        line_clean = line_clean.lower()

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


""" -----------------------------------------------------------------------------------------------
 Accessing Trefle API to fetch public image urls and additional infos, if available. Results 
 are stored in separate CSV file, ready to use. Do not run this script without having an api key!
----------------------------------------------------------------------------------------------- """
def call_trefle_api(df: DataFrame):
    load_dotenv()
    api_key = os.getenv("PLANT_API_KEY_TREFLE")

    for idx, row in df.iterrows():
        plant_name = row["plant name"].strip()
        print(f"Fetching additional infos for: {plant_name}")

        try:
            response = httpx.get(PLANT_API_BASE_URL_TREFLE,
                                 headers= {
                                     "Accept": "application/json"
                                 },
                                 params={
                                     "token": api_key,
                                     "filter[common_name]": plant_name
                                 })

            if response.status_code == 200:
                plant_data_json = response.json()
            else:
                continue

            if "data" in plant_data_json and len(plant_data_json["data"]) > 0:
                plant_id = plant_data_json["data"][0]["id"]

                details_response = httpx.get(PLANT_API_BASE_URL_TREFLE + f"/{plant_id}",
                                             headers= {
                                                 "Accept": "application/json"
                                             },
                                             params= {
                                                 "token": api_key
                                             })

                details_data_json = details_response.json()

                plant_infos = details_data_json["data"]
                image_url = plant_infos.get("image_url")

                df.at[idx, "image_url"] = image_url

        except Exception as e:
            print(f"Error Trefle API for {plant_name}: {e}")

    df.to_csv(DATASET_PATH_ENRICHED, index=False)


""" -----------------------------------------------------------------------------------------------
 Accessing Wikipedia API to fetch public image urls for substituting missing images as good as 
 possible.
----------------------------------------------------------------------------------------------- """
def call_wikipedia_api():
    load_dotenv()
    private_email = os.getenv("PRIVATE_EMAIL")
    df = pd.read_csv(DATASET_PATH_ENRICHED)

    for idx, row in df[df["image_url"].isna()].iterrows():
        plant_name = row["plant name"].strip()

        try:
            response = httpx.get(WIKIPEDIA_BASE_URL,
                                 headers={
                                     "User-Agent": f"Private Project ({private_email})"
                                 },
                                 params={
                                     "action": "query",
                                     "format": "json",
                                     "prop": "pageimages",
                                     "piprop": "thumbnail",
                                     "pithumbsize": 500,
                                     "titles": plant_name,
                                })

            if response.status_code == 200 and response.json():
                pages = response.json().get("query", {}).get("pages", {})

                if pages:
                    first = next(iter(pages.values()))
                    thumbnail = first.get("thumbnail", {})
                    image_url = thumbnail.get("source")

                    if image_url:
                        if image_url.startswith("//"):
                            image_url = "https:" + image_url

                        df.at[idx, "image_url"] = image_url

        except Exception as e:
            print(f"Error Wikipedia API for {plant_name}: {e}")

    df.to_csv(DATASET_PATH_ENRICHED, index=False)


""" -----------------------------------------------------------------------------------------------
 The cleaned dataset will be enriched with additional data from public APIs
----------------------------------------------------------------------------------------------- """
def enrich_dataset():
    df = pd.read_csv(DATASET_PATH_CLEAN)

    if "image_url" not in df.columns:
        df["image_url"] = None

    call_trefle_api(df)
    call_wikipedia_api()



def main():
    preprocess_dataset()
    get_rid_of_duplicates()
    enrich_dataset()
    print_infos()


if __name__ == "__main__":
    main()
