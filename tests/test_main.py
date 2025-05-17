import unittest
import os
import shutil
import base64
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
from src.main import (
    get_html_content,
    save_base64_image,
    save_image_from_url,
    process_image_url
)

class TestImageDownloader(unittest.TestCase):
    """Test cases for the image downloader functions."""

    def setUp(self):
        """Create a temporary directory for test files."""
        self.test_dir = "test_assets"
        os.makedirs(self.test_dir, exist_ok=True)
        self.test_url = "http://example.com"
        self.valid_base64 = (
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
        )

    def tearDown(self):
        """Remove temporary directory after tests."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    # Tests for get_html_content
    @patch('requests.get')
    def test_get_html_content_success(self, mock_get):
        """Test successful HTML content retrieval."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.text = "<html>Test</html>"
        mock_get.return_value = mock_response

        result = get_html_content(self.test_url)
        self.assertEqual(result, "<html>Test</html>")

    @patch('requests.get')
    def test_get_html_content_failure(self, mock_get):
        """Test failed HTML content retrieval."""
        mock_get.side_effect = requests.exceptions.RequestException("Error")

        result = get_html_content(self.test_url)
        self.assertIsNone(result)

    # Tests for save_base64_image
    def test_save_base64_image_valid(self):
        """Test saving a valid base64 image."""
        filename = save_base64_image(self.valid_base64, self.test_dir)
        self.assertEqual(filename, "image_from_base64.jpg")
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, filename)))

    def test_save_base64_image_invalid_format(self):
        """Test handling invalid base64 format."""
        filename = save_base64_image("invalid_base64", self.test_dir)
        self.assertIsNone(filename)

    def test_save_base64_image_invalid_data(self):
        """Test handling corrupted base64 data."""
        filename = save_base64_image("data:image/png;base64,INVALID_DATA", self.test_dir)
        self.assertIsNone(filename)

    # Tests for save_image_from_url
    @patch('requests.get')
    def test_save_image_from_url_success(self, mock_get):
        """Test successful image download from URL."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.content = b"test_image_data"
        mock_get.return_value = mock_response

        filename = save_image_from_url(
            "http://example.com/image.jpg",
            self.test_url,
            self.test_dir
        )
        self.assertEqual(filename, "image.jpg")
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, filename)))

    @patch('requests.get')
    def test_save_image_from_url_failure(self, mock_get):
        """Test failed image download."""
        mock_get.side_effect = requests.exceptions.RequestException("Error")

        filename = save_image_from_url(
            "http://example.com/image.jpg",
            self.test_url,
            self.test_dir
        )
        self.assertIsNone(filename)

    def test_save_image_from_url_invalid(self):
        """Test handling invalid URL."""
        filename = save_image_from_url(
            "javascript:alert(1)",
            self.test_url,
            self.test_dir
        )
        self.assertIsNone(filename)

    # Tests for process_image_url
    def test_process_image_url_base64(self):
        """Test processing base64 image."""
        img_tag = BeautifulSoup(
            f'<img src="{self.valid_base64}">',
            'html.parser'
        ).find('img')
        
        result = process_image_url(img_tag, self.test_url, self.test_dir)
        self.assertTrue(result)
        self.assertEqual(len(os.listdir(self.test_dir)), 1)

    @patch('requests.get')
    def test_process_image_url_normal(self, mock_get):
        """Test processing normal image URL."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.content = b"test_image_data"
        mock_get.return_value = mock_response

        img_tag = BeautifulSoup(
            '<img src="http://example.com/image.jpg">',
            'html.parser'
        ).find('img')
        
        result = process_image_url(img_tag, self.test_url, self.test_dir)
        self.assertTrue(result)

    def test_process_image_url_no_src(self):
        """Test handling img tag without src."""
        img_tag = BeautifulSoup('<img>', 'html.parser').find('img')
        result = process_image_url(img_tag, self.test_url, self.test_dir)
        self.assertFalse(result)

    def test_process_image_url_none_tag(self):
        """Test handling None img tag."""
        result = process_image_url(None, self.test_url, self.test_dir)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()