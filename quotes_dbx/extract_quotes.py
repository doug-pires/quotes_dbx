import os

import requests
from dotenv import load_dotenv

# Load Enviroment Variables
load_dotenv()

# Get API Key
API_KEY = os.getenv("API_KEY_NINJAS")


def extract_quote():
    category = "happiness"
    api_url = f"https://api.api-ninjas.com/v1/quotes?category={category}"
    response = requests.get(api_url, headers={"X-Api-Key": API_KEY})
    if response.status_code == requests.codes.ok:
        print(response.text)
    else:
        print("Error:", response.status_code, response.text)


def main():
    extract_quote()


if __name__ == "__main__":
    main()
