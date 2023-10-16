import json
import os
import random as rd
from datetime import datetime

import requests
from databricks.sdk.runtime import dbutils
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
    """
    Pick a random category from the provided list of words.

    Args:
        words_of_list (list): A list of categories from which a random category will be chosen.

    Returns:
        str: A randomly selected category from the list.

    This function takes a list of categories and selects a random category from the list.
    It returns the chosen category as a string.

    Example:
        category = pick_random_category(["age", "alone", "amazing"])
    """
    return rd.choice(words_of_list)


def extract_quote() -> list[dict]:
    """
    Extract a quote from a remote API and return it as a list of dictionaries.

    Returns:
        list[dict]: A list of dictionaries representing the extracted quote.

    Raises:
        Any exceptions raised by the underlying code when making the API request.

    This function sends an HTTP GET request to a remote API to retrieve a quote. If the
    API response has a successful status code (HTTP 200 OK), the response is parsed as JSON,
    and the quote is returned as a list of dictionaries. If the API request fails, an error
    is logged, including the status code and reason for the failure.

    Example:
        quote = extract_quote()
    """
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


def save_to_storage(path_dbfs: str, data: list[dict]) -> None:
    """
    Save a list of data as a JSON file to a specified location.

    Args:
        path_dbfs (str): The path where the JSON file will be saved.
        data (list): The data to be saved in JSON format.

    Returns:
        None

    This function takes a list of data and saves it as a JSON file at the specified location.
    It formats the data as JSON with indentation and sorts keys.
    If the save operation is successful, it logs an info message. If an exception occurs, it logs an error.

    Example:
        save_to_storage("/dbfs/data/", [1, 2, 3])
    """
    json_formatted = json.dumps(data)
    json_datetime = f"{path_dbfs}/data_json_{datetime.now().timestamp()}"
    try:
        dbutils.fs.put(json_datetime, json_formatted)
        logger.info("Saved to %s", path_dbfs)
    except AttributeError as e:
        logger.error(e)


def main():
    # It will be my entrypoint
    quote = extract_quote()
    print(quote)
    save_to_storage(path_dbfs="/mnt/json_dbx/", data=quote)


if __name__ == "__main__":
    main()
