"""This module uses the requests library to send a 
   POST request to a custom API. It includes error 
   handling for network issues and invalid responses."""

import requests
import dotenv
import base64
from src.log import logger


def post_img(img_path: str):
    """Send a POST request to a custom API endpoint.
    img_path: str: Path to the image to be sent in the request.
    Returns:
        dict: JSON response from the API if successful.
        bool: False if the request fails.
    """
    logger.info("Starting POST request to custom API endpoint")
    url = "https://intern.aiaxuropenings.com/v1/chat/completions"
    logger.debug("Target URL: %s", url)

    api_key = dotenv.get_key(dotenv.find_dotenv(), "OPENAI_API_KEY")
    logger.info("Using API key: %s", api_key)

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    logger.info("Headers set for request: %s", headers)


    with open(img_path, "rb") as img_file:
        logger.info("Image file opened successfully")
        
        # Codifica a imagem em base64
        base64_image = base64.b64encode(img_file.read()).decode('utf-8')
        
        payload = {
            "model": "microsoft-florence-2-large",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "<DETAILED_CAPTION>"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }
        
        # Corrigido: usar json=payload em vez de files=payload
        response = requests.post(url, headers=headers, json=payload)
        
        logger.debug("Response status code: %s", response.status_code)
        if response.status_code == 200:
            logger.info("POST request successful")
            logger.debug("Response data: %s", response.json())
            return response.json()
        else:
            logger.error("POST request failed with status code: %s", response.status_code)
            logger.error("Response content: %s", response.content)
            return False
