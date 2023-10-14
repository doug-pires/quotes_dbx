import os

import requests
from dotenv import load_dotenv

from quotes_dbx.config_logging import get_logger

logger = get_logger(__name__)


# Load Enviroment Variables
load_dotenv()

# Get API Key
API_KEY = os.getenv("API_KEY_NINJAS")


def extract_quote():
    category = "happiness"
    api_url = f"https://api.api-ninjas.com/v1/quotes?category={category}"
    response = requests.get(api_url, headers={"X-Api-Key": API_KEY})
    if response.status_code == requests.codes.ok:
        quote = response.text
        return quote
    else:
        logger.error(
            "Status Code: %s - Reason: %s", response.status_code, response.text
        )


def main():
    extract_quote()


if __name__ == "__main__":
    main()
