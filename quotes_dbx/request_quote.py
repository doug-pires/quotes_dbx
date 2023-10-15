import json
import os
import random as rd
from datetime import datetime

import requests
from dotenv import load_dotenv

from quotes_dbx.config_logging import get_logger

logger = get_logger(__name__)


# Load Enviroment Variables
load_dotenv()

# Get API Key
API_KEY = os.getenv("API_KEY_NINJAS")


category_list = [
    "age",
    "alone",
    "amazing",
    "anger",
    "architecture",
    "art",
    "attitude",
    "beauty",
    "best",
    "birthday",
]


def pick_random_category(words_of_list: list) -> str:
    return rd.choice(words_of_list)


def extract_quote() -> list:
    category = pick_random_category(category_list)
    api_url = f"https://api.api-ninjas.com/v1/quotes?category={category}"
    response = requests.get(api_url, headers={"X-Api-Key": API_KEY})
    if response.status_code == requests.codes.ok:
        quote = response.json()
        return quote
    else:
        logger.error(
            "Status Code: %s - Reason: %s", response.status_code, response.text
        )


def save_to_storage(path_dbfs: str, data: list) -> None:
    json_formatted = json.dumps(data, indent=4, sort_keys=True)
    json_datetime = f"{path_dbfs}data_json_{datetime.now().timestamp()}"
    try:
        dbutils.fs.put(json_datetime, json_formatted)
        logger.info("Saved to %s", path_dbfs)
    except AttributeError as e:
        logger.error(e)


def main():
    quote = extract_quote()
    save_to_storage(path_dbfs="/mnt/json_dbx/", data=quote)


if __name__ == "__main__":
    main()
