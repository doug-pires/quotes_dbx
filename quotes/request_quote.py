import json
import random as rd
from datetime import datetime

import requests
from databricks.sdk import WorkspaceClient

from quotes.config_logging import get_stream_logger
from quotes.provide_config import path_landing_quotes_dbx

logger = get_stream_logger(__name__)


def authenticate_databricks(current_profile: str):
    """
    Authenticate with Databricks using the specified profile.

    Parameters:
        current_profile (str): The name of the Databricks profile to use for authentication.
                                This profile should be configured in the file .databrickscfg.

    You can add host and token as Databricks Secrets

    Returns:
        WorkspaceClient: An authenticated Databricks WorkspaceClient instance.

    Example:
        To authenticate using a profile named "KIPROFILE":
        >>> client = authenticate_databricks("KIPROFILE")
    """
    # Configure the Profile
    # Reading from the
    # You can add your profile here configured in the file .databrickscfg

    w = WorkspaceClient(profile=current_profile)

    return w


# Get API Key
API_KEY = w.dbutils.secrets.get(scope="api_keys", key="ninjas")
# os.getenv("API_KEY_NINJAS")


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

    if data is not None:
        authenticate_databricks(profile="KIPROFILE")
        json_formatted = json.dumps(data)
        json_datetime = f"{path_dbfs}/data_json_{datetime.now().timestamp()}"
        try:
            w.dbutils.fs.put(json_datetime, json_formatted)
            logger.info("Saved to %s", path_dbfs)
        except AttributeError as e:
            logger.error(e)
    else:
        logger.info("Data returned None")


def main():  # pragma: no cover
    quote = extract_quote()
    print(quote)
    save_to_storage(path_dbfs=path_landing_quotes_dbx, data=quote)
