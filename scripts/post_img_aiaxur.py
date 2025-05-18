"""This module uses the requests library to send a 
   POST request to a custom API. It includes error 
   handling for network issues and invalid responses."""

import requests
import dotenv
from src.log import logger


def post_img_api_aiaxur(raw_json: dict):
    """Send a POST request to a custom API endpoint.
    img_path: str: Path to the image to be sent in the request.
    Returns:
        raw json: JSON response from the API if successful.
    """
    logger.info("Starting POST request to custom API endpoint")
    url = "https://intern.aiaxuropenings.com/api/submit-response"
    logger.info("Target URL: %s", url)

    api_key = dotenv.get_key(dotenv.find_dotenv(), "OPENAI_API_KEY")
    logger.info("Using API key: %s", api_key)

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    submit_response = requests.post(url=url, headers=headers, json=raw_json)

    if submit_response.status_code == 200:
        logger.info("Pass interview")
        logger.debug("Response data: %s", submit_response.json())
        return True
    else:
        logger.error("Try again")
        return False
