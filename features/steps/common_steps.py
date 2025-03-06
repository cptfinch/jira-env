"""
Common step definitions for Jira tests

This file contains step definitions that are shared across multiple feature files.
"""
from behave import given, when, then
from unittest.mock import patch, MagicMock
import os
from core import JiraInterface

# Environment variable setup steps
@given('the Jira environment variables are set')
def step_env_vars_set(context):
    """Set up environment variables for testing"""
    context.env_patcher = patch.dict('os.environ', {
        'JIRA_BASE_URL': 'https://test-jira.example.com',
        'JIRA_API_TOKEN': 'test-token-123'
    })
    context.env_patcher.start()

@given('I have set the JIRA_BASE_URL environment variable to "{url}"')
def step_set_base_url(context, url):
    """Set the JIRA_BASE_URL environment variable"""
    os.environ['JIRA_BASE_URL'] = url
    context.expected_url = url

@given('I have set the JIRA_API_TOKEN environment variable')
def step_set_api_token(context):
    """Verify that the JIRA_API_TOKEN environment variable is set"""
    # We don't set it here, we just verify it's already set
    assert 'JIRA_API_TOKEN' in os.environ, "JIRA_API_TOKEN environment variable is not set"
    assert os.environ['JIRA_API_TOKEN'], "JIRA_API_TOKEN environment variable is empty"

@given('I have set both JIRA_BASE_URL and JIRA_API_TOKEN environment variables')
def step_set_both_vars(context):
    """Verify that both environment variables are set"""
    # Verify JIRA_BASE_URL
    assert 'JIRA_BASE_URL' in os.environ, "JIRA_BASE_URL environment variable is not set"
    assert os.environ['JIRA_BASE_URL'], "JIRA_BASE_URL environment variable is empty"
    
    # Verify JIRA_API_TOKEN
    assert 'JIRA_API_TOKEN' in os.environ, "JIRA_API_TOKEN environment variable is not set"
    assert os.environ['JIRA_API_TOKEN'], "JIRA_API_TOKEN environment variable is empty"

# JiraInterface creation steps
@when('I create a JiraInterface instance')
def step_create_interface(context):
    """Create a JiraInterface instance using environment variables"""
    context.jira = JiraInterface()

@then('the instance should use the environment variables')
def step_check_env_vars(context):
    """Check that the instance is using the environment variables"""
    assert context.jira.base_url == os.environ.get('JIRA_BASE_URL')
    assert context.jira.api_token == os.environ.get('JIRA_API_TOKEN')
    # Clean up if needed
    if hasattr(context, 'env_patcher') and context.env_patcher:
        context.env_patcher.stop()

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