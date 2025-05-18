"""This script downloads an image from a 
provided URL, whether it's a normal URL or a base64 encoded image."""

import os
from bs4 import BeautifulSoup
from utils.controler_functions import (
    process_image_url,
    get_html_content,
)
from .log import logger
from scripts.post_img import post_img
from scripts.post_img_aiaxur import post_img_api_aiaxur as post_img_aiaxur

def main():
    """Main function to execute the image downloading process."""
    logger.info("Starting image download process")
    url = (
        "https://intern.aiaxuropenings.com/scrape/7dbfdfa6-b88b-4339-9d91-dc6dd9ed2448"
    )
    save_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets"))

    logger.info("Target URL: %s", url)
    logger.debug("Save path: %s", save_path)

    logger.info("Fetching HTML content")
    html_content = get_html_content(url)
    if not html_content:
        logger.error("Aborting process due to HTML fetch failure")
        return

    logger.info("Parsing HTML content")
    soup = BeautifulSoup(html_content, "html.parser")
    img_tag = soup.find("img")

    if not img_tag:
        logger.warning("No image tag found in HTML content")
        return

    logger.info("Processing image tag")
    result = process_image_url(img_tag, url, save_path)

    if result:
        logger.info("Image download process completed successfully")
        response = post_img(r".\assets\image_from_base64.jpg")
        if response:
            post_img_aiaxur(response)
    else:
        logger.error("Image download process failed")


if __name__ == "__main__":
    main()
