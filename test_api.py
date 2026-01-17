import unittest
from unittest.mock import patch, MagicMock
import json
import urllib.request
from check_snow_status import get_snow_status

class TestSnowStatus(unittest.TestCase):

    @patch('urllib.request.urlopen')
    def test_get_snow_status_completed(self, mock_urlopen):
        # Mock response for a completed section
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = json.dumps({
            "features": [
                {
                    "attributes": {
                        "STATUS": "COMPLETED",
                        "SECTIONNUMBER": "14"
                    }
                }
            ]
        }).encode('utf-8')
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        status = get_snow_status("14")
        self.assertEqual(status, "COMPLETED")

    @patch('urllib.request.urlopen')
    def test_get_snow_status_not_found(self, mock_urlopen):
        # Mock response for a non-existent section
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = json.dumps({
            "features": []
        }).encode('utf-8')
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        status = get_snow_status("999")
        self.assertEqual(status, "NOT FOUND")

    @patch('urllib.request.urlopen')
    def test_get_snow_status_api_error(self, mock_urlopen):
        # Mock response for an API error
        mock_response = MagicMock()
        mock_response.status = 500
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        status = get_snow_status("14")
        self.assertTrue(status.startswith("ERROR"))

if __name__ == '__main__':
    unittest.main()
