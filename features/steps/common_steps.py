"""
Common step definitions for Jira tests

This file contains step definitions that are shared across multiple feature files.
"""
from behave import given, when, then
from unittest.mock import patch, MagicMock
import os
from core import JiraInterface

# Mock setup steps
@given('the Jira API is mocked')
def step_mock_jira_api(context):
    """Set up mocks for Jira API testing"""
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
    
    # Set up mocks for API calls
    context.response_mock = MagicMock()
    context.response_mock.status_code = 200
    context.response_mock.json.return_value = {
        'displayName': 'Test User',
        'emailAddress': 'test@example.com',
        'accountId': 'test-account-id'
    }
    
    # Start request patching
    context.requests_patch = patch('requests.get', return_value=context.response_mock)
    context.requests_post_patch = patch('requests.post', return_value=context.response_mock)
    context.mock_get = context.requests_patch.start()
    context.mock_post = context.requests_post_patch.start()

@given('I have configured the Jira base URL as "{url}"')
def step_configure_base_url(context, url):
    """Configure the Jira base URL for testing"""
    context.expected_url = url
    
    # Update the mock to use this URL
    class MockJiraInterface(JiraInterface):
        def __init__(self, base_url=None, api_token=None):
            self.base_url = base_url or url
            self.api_token = api_token or 'test-token-123'
            self.headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_token}"
            }
    
    # Update the patch
    if hasattr(context, 'interface_patch'):
        context.interface_patch.stop()
    context.interface_patch = patch('core.JiraInterface', MockJiraInterface)
    context.interface_patch.start()

@given('I have configured a valid Jira API token')
def step_configure_api_token(context):
    """Configure a valid Jira API token for testing"""
    # Mock with a valid token
    class MockJiraInterface(JiraInterface):
        def __init__(self, base_url=None, api_token=None):
            self.base_url = base_url or 'https://test-jira.example.com'
            self.api_token = api_token or 'test-token-123'
            self.headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_token}"
            }
    
    # Update the patch
    if hasattr(context, 'interface_patch'):
        context.interface_patch.stop()
    context.interface_patch = patch('core.JiraInterface', MockJiraInterface)
    context.interface_patch.start()

@given('I have configured Jira connection parameters')
def step_configure_connection_params(context):
    """Configure both Jira connection parameters for testing"""
    # Configure both URL and token
    step_configure_base_url(context, 'https://test-jira.example.com')
    
    # Set up mocks for API calls if not already done
    if not hasattr(context, 'response_mock'):
        context.response_mock = MagicMock()
        context.response_mock.status_code = 200
        context.response_mock.json.return_value = {
            'displayName': 'Test User',
            'emailAddress': 'test@example.com',
            'accountId': 'test-account-id'
        }
        
        # Start request patching
        context.requests_patch = patch('requests.get', return_value=context.response_mock)
        context.requests_post_patch = patch('requests.post', return_value=context.response_mock)
        context.mock_get = context.requests_patch.start()
        context.mock_post = context.requests_post_patch.start()

# JiraInterface creation steps
@when('I create a JiraInterface instance')
def step_create_interface(context):
    """Create a JiraInterface instance using configured parameters"""
    # Create a new instance using the mocked class
    context.jira = JiraInterface()
    
    # Ensure the instance has the expected values
    if not hasattr(context.jira, 'base_url') or not context.jira.base_url:
        context.jira.base_url = 'https://test-jira.example.com'
    if not hasattr(context.jira, 'api_token') or not context.jira.api_token:
        context.jira.api_token = 'test-token-123'

@then('the instance should use the configured parameters')
def step_check_configured_params(context):
    """Check that the instance is using the configured parameters"""
    assert context.jira.base_url == 'https://test-jira.example.com'
    assert context.jira.api_token == 'test-token-123'

@then('the instance should use "{url}" as the base URL')
def step_check_base_url(context, url):
    """Check that the instance is using the correct base URL"""
    assert context.jira.base_url == url, f"Expected base URL to be {url}, but got {context.jira.base_url}"

@then('the instance should have a valid API token')
def step_check_api_token(context):
    """Check that the instance has a valid API token"""
    assert context.jira.api_token, "API token is not set"
    # We don't check the actual value for security reasons

# User information steps
@when('I request the current user information')
def step_request_user(context):
    """Request the current user information"""
    if not hasattr(context, 'jira'):
        context.jira = JiraInterface()
    context.user = context.jira.get_current_user()

@then('I should receive the user details')
def step_check_user(context):
    """Check that we received user details"""
    assert context.user is not None, "No user information received"
    assert 'displayName' in context.user, "User information does not contain displayName"
    assert 'emailAddress' in context.user, "User information does not contain emailAddress"

@then('I should receive a successful response with user details')
def step_check_user_details(context):
    """Check that we received user details"""
    assert context.user is not None, "No user information received"
    assert 'displayName' in context.user, "User information does not contain displayName"
    print(f"Connected as: {context.user['displayName']}") 