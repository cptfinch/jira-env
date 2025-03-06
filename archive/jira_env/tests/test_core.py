"""
Tests for the core module
"""

import unittest
from unittest.mock import patch, MagicMock

from jira_env.core import JiraInterface


class TestJiraInterface(unittest.TestCase):
    """Test cases for the JiraInterface class"""
    
    @patch('jira_env.core.requests.get')
    def test_get_current_user(self, mock_get):
        """Test the get_current_user method"""
        # Setup mock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"name": "test_user", "accountId": "123456"}
        mock_get.return_value = mock_response
        
        # Create instance with mock token
        jira = JiraInterface(api_token="test_token")
        
        # Call the method
        result = jira.get_current_user()
        
        # Assertions
        self.assertEqual(result["name"], "test_user")
        self.assertEqual(result["accountId"], "123456")
        mock_get.assert_called_once()


if __name__ == '__main__':
    unittest.main() 