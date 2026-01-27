import unittest
from unittest.mock import patch, MagicMock
from src.services.browser import BrowserService

class TestIteration4(unittest.TestCase):
    @patch('src.services.browser.subprocess.Popen')
    def test_browser_open_linux(self, mock_popen):
        # Mock sys.platform to linux
        with patch('sys.platform', 'linux'):
            service = BrowserService()
            result = service.open_url("http://google.com")
            self.assertTrue(result)
            mock_popen.assert_called_with(['xdg-open', "http://google.com"])

if __name__ == "__main__":
    unittest.main()
