"""
This module contains unit tests for utility functions related to image processing and HTML content fetching.
It includes tests for:
- Fetching HTML content from a URL
- Saving base64 encoded images
- Downloading images from URLs (both absolute and relative)
- Processing image URLs (base64 and standard)
- Handling invalid image URLs and tags
"""
import os
import pytest
import requests
from src.log import logger
from unittest.mock import patch, Mock
from urllib.parse import urljoin
from utils.controler_functions import (
    get_html_content,
    save_base64_image,
    save_image_from_url,
    process_image_url,
)


# Test data
TEST_DIR = "test_images"
TEST_URL = "http://example.com"
VALID_HTML_URL = "http://example.com/page"
INVALID_HTML_URL = "http://invalid.url"
BASE64_IMAGE = (
    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk"
    "YPj/HwADBwIAMCbHYQAAAABJRU5ErkJggg=="
)
INVALID_BASE64 = "data:image/png;base64,invalid!!"
RELATIVE_IMG_URL = "/image.jpg"
ABSOLUTE_IMG_URL = "http://example.com/image.jpg"
INVALID_IMG_URL = "ftp://example.com/image.jpg"


@pytest.fixture(scope="module", autouse=True)
def setup_teardown():
    """Create and cleanup test directory."""
    os.makedirs(TEST_DIR, exist_ok=True)
    yield
    for file in os.listdir(TEST_DIR):
        os.remove(os.path.join(TEST_DIR, file))
    os.rmdir(TEST_DIR)


def test_get_html_content_success():
    """Test successful HTML content fetch."""
    logger.info("Testing get_html_content with valid URL")
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "<html>content</html>"

        result = get_html_content(VALID_HTML_URL)
        assert result == "<html>content</html>"
        logger.debug("Test passed: get_html_content returned expected content")


def test_get_html_content_failure():
    """Test failed HTML content fetch."""
    logger.info("Testing get_html_content with invalid URL")
    with patch("requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.RequestException("Error")

        result = get_html_content(INVALID_HTML_URL)
        assert result is None
        logger.debug("Test passed: get_html_content returned None on failure")


def test_save_base64_image_success():
    """Test successful base64 image save."""
    logger.info("Testing save_base64_image with valid data")
    filename = save_base64_image(BASE64_IMAGE, TEST_DIR)

    assert filename is not None
    assert os.path.exists(os.path.join(TEST_DIR, filename))
    logger.debug("Test passed: base64 image saved successfully")


def test_save_base64_image_invalid():
    """Test invalid base64 image handling."""
    logger.info("Testing save_base64_image with invalid data")
    filename = save_base64_image(INVALID_BASE64, TEST_DIR)

    assert filename is None
    logger.debug("Test passed: invalid base64 correctly handled")


def test_save_image_from_url_absolute():
    """Test absolute image URL download."""
    logger.info("Testing save_image_from_url with absolute URL")
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = b"image_data"

        filename = save_image_from_url(ABSOLUTE_IMG_URL, TEST_URL, TEST_DIR)
        assert filename == "image.jpg"
        logger.debug("Test passed: absolute URL image saved")


def test_save_image_from_url_relative():
    """Test relative image URL download."""
    logger.info("Testing save_image_from_url with relative URL")
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = b"image_data"

        filename = save_image_from_url(RELATIVE_IMG_URL, TEST_URL, TEST_DIR)
        assert filename == "image.jpg"
        logger.debug("Test passed: relative URL image saved")


def test_save_image_from_url_invalid():
    """Test invalid image URL handling."""
    logger.info("Testing save_image_from_url with invalid URL")
    filename = save_image_from_url(INVALID_IMG_URL, TEST_URL, TEST_DIR)

    assert filename is None
    logger.debug("Test passed: invalid URL correctly handled")


def test_process_image_url_base64():
    """Test base64 image processing."""
    logger.info("Testing process_image_url with base64 image")

    # Criamos um mock que implementa tanto get() quanto __getitem__
    class MockTag:
        def __init__(self, src_value):
            self.src_value = src_value

        def __getitem__(self, key):
            if key == "src":
                return self.src_value
            raise KeyError(key)

        def get(self, key, default=None):
            if key == "src":
                return self.src_value
            return default

    mock_tag = MockTag(BASE64_IMAGE)
    result = process_image_url(mock_tag, TEST_URL, TEST_DIR)
    assert result is True
    logger.debug("Test passed: base64 image processed successfully")


def test_process_image_url_standard():
    """Test standard image URL processing."""
    logger.info("Testing process_image_url with standard URL")
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = b"image_data"

        class MockTag:
            def __init__(self, src_value):
                self.src_value = src_value

            def __getitem__(self, key):
                if key == "src":
                    return self.src_value
                raise KeyError(key)

            def get(self, key, default=None):
                if key == "src":
                    return self.src_value
                return default

        mock_tag = MockTag(ABSOLUTE_IMG_URL)
        result = process_image_url(mock_tag, TEST_URL, TEST_DIR)
        assert result is True
        logger.debug("Test passed: standard URL image processed")


def test_process_image_url_invalid():
    """Test invalid image tag handling."""
    logger.info("Testing process_image_url with invalid tag")
    mock_tag = Mock()
    mock_tag.get.return_value = None

    result = process_image_url(mock_tag, TEST_URL, TEST_DIR)
    assert result is False
    logger.debug("Test passed: invalid tag correctly handled")
