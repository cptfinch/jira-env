"""
Step definitions for Jira configuration tests
"""
from behave import given, when, then
import os
from core import JiraInterface

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
    
    # Create the JiraInterface instance
    context.jira = JiraInterface()

@when('I create a JiraInterface instance for config testing')
def step_create_interface_config(context):
    """Create a JiraInterface instance for configuration testing"""
    context.jira = JiraInterface()

@when('I request the current user information for config testing')
def step_request_user_info_config(context):
    """Request the current user information for configuration testing"""
    if not hasattr(context, 'jira'):
        context.jira = JiraInterface()
    context.user_info = context.jira.get_current_user()

@then('the instance should use "{url}" as the base URL')
def step_check_base_url(context, url):
    """Check that the instance is using the correct base URL"""
    assert context.jira.base_url == url, f"Expected base URL to be {url}, but got {context.jira.base_url}"

@then('the instance should have a valid API token')
def step_check_api_token(context):
    """Check that the instance has a valid API token"""
    assert context.jira.api_token, "API token is not set"
    # We don't check the actual value for security reasons

@then('I should receive a successful response with user details')
def step_check_user_details(context):
    """Check that we received user details"""
    assert context.user_info is not None, "No user information received"
    assert 'displayName' in context.user_info, "User information does not contain displayName"
    print(f"Connected as: {context.user_info['displayName']}") 