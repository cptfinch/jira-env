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

# Authentication error steps
@given('I have an invalid API token')
def step_invalid_token(context):
    """Set up environment with an invalid API token"""
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
    """Check that we received an error response"""
    assert context.user is None
    
    # Clean up
    patch.stopall() 