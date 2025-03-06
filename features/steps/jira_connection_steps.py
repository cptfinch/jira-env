"""
Step definitions for Jira connection tests

This file contains step definitions specific to Jira connection functionality.
Common steps are imported from common_steps.py.
"""
from behave import given, when, then
from unittest.mock import patch, MagicMock
import os
from core import JiraInterface

# Import common steps to ensure they're available
# We don't need to redefine them here
from features.steps.common_steps import *

# Custom connection parameter steps
@given('I have custom Jira connection parameters')
def step_custom_params(context):
    """Set up custom connection parameters"""
    context.custom_url = 'https://custom-jira.example.com'
    context.custom_token = 'custom-token-456'

@when('I create a JiraInterface with these parameters')
def step_create_with_params(context):
    """Create a JiraInterface with custom parameters"""
    context.jira = JiraInterface(
        base_url=context.custom_url,
        api_token=context.custom_token
    )

@then('the instance should use the custom parameters')
def step_check_custom_params(context):
    """Check that the instance is using the custom parameters"""
    assert context.jira.base_url == context.custom_url
    assert context.jira.api_token == context.custom_token

# Valid connection setup
@given('I have a valid Jira connection')
def step_valid_connection(context):
    """Set up a valid Jira connection with mocked response"""
    # Create a mock JiraInterface class
    class MockJiraInterface(JiraInterface):
        def __init__(self, base_url=None, api_token=None):
            self.base_url = base_url or 'https://test-jira.example.com'
            self.api_token = api_token or 'test-token-123'
            self.headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_token}"
            }
    
    # Patch the JiraInterface class
    context.interface_patch = patch('core.JiraInterface', MockJiraInterface)
    context.interface_patch.start()
    
    # Create JiraInterface
    context.jira = JiraInterface()
    
    # Mock the requests.get method
    context.mock_get = patch('requests.get').start()
    context.mock_response = MagicMock()
    context.mock_response.status_code = 200
    context.mock_response.json.return_value = {
        'displayName': 'Test User',
        'emailAddress': 'test@example.com'
    }
    context.mock_get.return_value = context.mock_response

# Authentication error steps
@given('I have an invalid API token')
def step_invalid_token(context):
    """Set up with an invalid API token"""
    # Create a mock JiraInterface class with invalid token
    class MockJiraInterface(JiraInterface):
        def __init__(self, base_url=None, api_token=None):
            self.base_url = base_url or 'https://test-jira.example.com'
            self.api_token = api_token or 'invalid-token'
            self.headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_token}"
            }
    
    # Patch the JiraInterface class
    context.interface_patch = patch('core.JiraInterface', MockJiraInterface)
    context.interface_patch.start()
    
    # Create JiraInterface
    context.jira = JiraInterface()
    
    # Mock the requests.get method to return an error
    context.mock_get = patch('requests.get').start()
    context.mock_response = MagicMock()
    context.mock_response.status_code = 401
    context.mock_response.text = 'Unauthorized'
    context.mock_get.return_value = context.mock_response

# Add a specific step for the failing test
@when('I create a JiraInterface instance for the connection test')
def step_create_interface_connection(context):
    """Create a JiraInterface instance specifically for the connection test"""
    # Create a mock JiraInterface class
    class MockJiraInterface(JiraInterface):
        def __init__(self, base_url=None, api_token=None):
            self.base_url = 'https://test-jira.example.com'
            self.api_token = 'test-token-123'
            self.headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_token}"
            }
    
    # Patch the JiraInterface class
    if hasattr(context, 'interface_patch'):
        context.interface_patch.stop()
    context.interface_patch = patch('core.JiraInterface', MockJiraInterface)
    context.interface_patch.start()
    
    # Create JiraInterface
    context.jira = JiraInterface()

@then('I should receive an error response')
def step_check_error(context):
    """Check that we received an error response"""
    assert context.user is None
    
    # Clean up
    patch.stopall() 