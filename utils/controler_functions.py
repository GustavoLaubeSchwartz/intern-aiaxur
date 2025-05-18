"""This module is responsible for downloading images from a given URL.
It handles both base64 encoded images and standard image URLs."""

import re
import os
import base64
import urllib.parse
import requests
from src.log import logger


def get_html_content(url):
    """
    Fetch HTML content from a given URL.

    Args:
        url (str): URL to fetch HTML from.

    Returns:
        str: HTML content if successful, None otherwise.
    """
    logger.info("Initiating HTML content fetch from: %s", url)
    try:
        response = requests.get(url, timeout=10)
        logger.debug("Response status code: %s", response.status_code)
        response.raise_for_status()
        logger.info("HTML content successfully fetched")
        return response.text
    except requests.exceptions.RequestException as error:
        logger.error("Failed to fetch HTML content: %s", error, exc_info=True)
        return None


def save_base64_image(base64_str, save_path):
    """
    Save a base64 encoded image to file.

    Args:
        base64_str (str): Base64 encoded image data.
        save_path (str): Directory path to save the image.

    Returns:
        str: Filename if successful, None otherwise.
    """
    logger.info("Processing base64 encoded image")
    try:
        match = re.match(r"data:image/[^;]+;base64,(.*)", base64_str)
        if not match:
            logger.error("Invalid base64 image format - missing prefix")
            return None

        logger.debug("Base64 format validated, decoding image data")
        img_data = base64.b64decode(match.group(1))
        filename = "image_from_base64.jpg"
        full_path = os.path.join(save_path, filename)

        logger.info("Attempting to save image to: %s", full_path)
        with open(full_path, "wb") as img_file:
            img_file.write(img_data)

        logger.info("Base64 image successfully saved as: %s", filename)
        return filename
    except (base64.binascii.Error, OSError) as error:
        logger.error("Failed to save base64 image: %s ", error, exc_info=True)
        return None


def save_image_from_url(img_url, base_url, save_path):
    """
    Download and save an image from a normal URL.

    Args:
        img_url (str): Image URL (absolute or relative).
        base_url (str): Base URL for resolving relative URLs.
        save_path (str): Directory path to save the image.

    Returns:
        str: Filename if successful, None otherwise.
    """
    logger.info("Processing image URL: %s", img_url)
    try:
        absolute_url = urllib.parse.urljoin(base_url, img_url)
        if not absolute_url.startswith(("http://", "https://")):
            logger.error("Invalid URL scheme: %s", absolute_url)
            return None

        logger.debug("Resolved absolute URL: %s", absolute_url)
        response = requests.get(absolute_url, timeout=10)
        response.raise_for_status()

        filename = (
            os.path.basename(urllib.parse.urlparse(absolute_url).path)
            or "downloaded_image.jpg"
        )
        full_path = os.path.join(save_path, filename)

        logger.info("Saving image to: %s", full_path)
        with open(full_path, "wb") as img_file:
            img_file.write(response.content)

        logger.info("Image successfully saved as: %s", filename)
        return filename
    except requests.exceptions.RequestException as error:
        logger.error("Failed to download image: %s", error, exc_info=True)
        return None


def process_image_url(img_tag, base_url, save_path):
    """
    Process an image tag and download the image.

    Args:
        img_tag (bs4.element.Tag): BeautifulSoup img tag object.
        base_url (str): Base URL for resolving relative URLs.
        save_path (str): Directory path to save the image.

    Returns:
        bool: True if image was processed successfully, False otherwise.
    """
    if not img_tag or not img_tag.get("src"):
        logger.error("No valid img tag or src attribute found")
        return False

    src = img_tag["src"]
    label_logger = "base64" if src.startswith("data:image") else src
    logger.debug(
        "Processing image source: %s",
        label_logger,
    )

    if src.startswith("data:image"):
        logger.info("Processing base64 encoded image")
        return save_base64_image(src, save_path) is not None

    logger.info("Processing standard image URL")
    return save_image_from_url(src, base_url, save_path) is not None
