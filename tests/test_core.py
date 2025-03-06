"""
Tests for the core module
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import core
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core import JiraInterface


class TestJiraInterface(unittest.TestCase):
    """Test cases for the JiraInterface class"""
    
    @patch('core.requests.get')
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
    
    @patch('core.requests.post')
    def test_search_issues(self, mock_post):
        """Test the search_issues method"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "issues": [
                {"id": "10001", "key": "TEST-1", "fields": {"summary": "Test issue 1"}},
                {"id": "10002", "key": "TEST-2", "fields": {"summary": "Test issue 2"}}
            ],
            "total": 2,
            "maxResults": 50,
            "startAt": 0
        }
        mock_post.return_value = mock_response
        
        # Create instance with mock token
        jira = JiraInterface(api_token="test_token")
        
        # Call the method with a test JQL query
        jql = "project = TEST AND assignee = currentUser()"
        result = jira.search_issues(jql, max_results=50)
        
        # Assertions
        self.assertEqual(len(result["issues"]), 2)
        self.assertEqual(result["total"], 2)
        self.assertEqual(result["issues"][0]["key"], "TEST-1")
        self.assertEqual(result["issues"][1]["key"], "TEST-2")
        
        # Verify the correct API call was made
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertIn("json", kwargs)
        self.assertEqual(kwargs["json"]["jql"], jql)
        self.assertEqual(kwargs["json"]["maxResults"], 50)


if __name__ == '__main__':
    unittest.main() 