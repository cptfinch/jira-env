"""
Step definitions for Jira configuration tests

This file contains step definitions specific to Jira configuration functionality.
Common steps are imported from common_steps.py.
"""
from behave import given, when, then
import os
from core import JiraInterface

# Import common steps to ensure they're available
from features.steps.common_steps import *

# Config-specific steps
@when('I create a JiraInterface instance for config testing')
def step_create_interface_config(context):
    """Create a JiraInterface instance specifically for configuration testing"""
    # This is a wrapper around the common step to provide a more descriptive name
    # for the config feature file
    if not hasattr(context, 'jira'):
        context.jira = JiraInterface()

@when('I request the current user information for config testing')
def step_request_user_info_config(context):
    """Request the current user information specifically for configuration testing"""
    # This is a wrapper around the common step to provide a more descriptive name
    # for the config feature file
    if not hasattr(context, 'jira'):
        context.jira = JiraInterface()
    context.user = context.jira.get_current_user() 