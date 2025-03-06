"""
Step definitions for Jira connection tests
"""
from behave import given, when, then
from unittest.mock import patch, MagicMock
import os
from core import JiraInterface

@given('the Jira environment variables are set')
def step_env_vars_set(context):
    # Set up environment variables for testing
    context.env_patcher = patch.dict('os.environ', {
        'JIRA_BASE_URL': 'https://test-jira.example.com',
        'JIRA_API_TOKEN': 'test-token-123'
    })
    context.env_patcher.start()

@when('I create a JiraInterface instance')
def step_create_interface(context):
    context.jira = JiraInterface()

@then('the instance should use the environment variables')
def step_check_env_vars(context):
    assert context.jira.base_url == 'https://test-jira.example.com'
    assert context.jira.api_token == 'test-token-123'
    # Clean up
    context.env_patcher.stop()

@given('I have custom Jira connection parameters')
def step_custom_params(context):
    context.custom_url = 'https://custom-jira.example.com'
    context.custom_token = 'custom-token-456'

@when('I create a JiraInterface with these parameters')
def step_create_with_params(context):
    context.jira = JiraInterface(
        base_url=context.custom_url,
        api_token=context.custom_token
    )

@then('the instance should use the custom parameters')
def step_check_custom_params(context):
    assert context.jira.base_url == context.custom_url
    assert context.jira.api_token == context.custom_token

@given('I have a valid Jira connection')
def step_valid_connection(context):
    # Set up environment variables
    context.env_patcher = patch.dict('os.environ', {
        'JIRA_BASE_URL': 'https://test-jira.example.com',
        'JIRA_API_TOKEN': 'test-token-123'
    })
    context.env_patcher.start()
    
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

@when('I request the current user information')
def step_request_user(context):
    context.user = context.jira.get_current_user()

@then('I should receive the user details')
def step_check_user(context):
    assert context.user is not None
    assert context.user['displayName'] == 'Test User'
    assert context.user['emailAddress'] == 'test@example.com'
    
    # Verify the request
    context.mock_get.assert_called_once_with(
        'https://test-jira.example.com/rest/api/2/myself',
        headers=context.jira.headers
    )
    
    # Clean up
    patch.stopall()

@given('I have an invalid API token')
def step_invalid_token(context):
    # Set up environment variables with invalid token
    context.env_patcher = patch.dict('os.environ', {
        'JIRA_BASE_URL': 'https://test-jira.example.com',
        'JIRA_API_TOKEN': 'invalid-token'
    })
    context.env_patcher.start()
    
    # Create JiraInterface
    context.jira = JiraInterface()
    
    # Mock the requests.get method to return an error
    context.mock_get = patch('requests.get').start()
    context.mock_response = MagicMock()
    context.mock_response.status_code = 401
    context.mock_response.text = 'Unauthorized'
    context.mock_get.return_value = context.mock_response

@then('I should receive an error response')
def step_check_error(context):
    assert context.user is None
    
    # Clean up
    patch.stopall() 