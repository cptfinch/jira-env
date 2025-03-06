"""
Environment setup for Behave tests

This file contains hooks that run before and after certain events during testing.
"""
from unittest.mock import patch
import os

def before_all(context):
    """
    Runs before all tests.
    """
    # Set up any global configuration here
    print("Starting Jira API tests...")
    
    # Set the BEHAVE_TESTING environment variable to indicate we're in a test environment
    os.environ['BEHAVE_TESTING'] = 'true'
    
    # Ensure we have a place to store test data
    context.test_data = {}

def after_all(context):
    """
    Runs after all tests.
    """
    print("All Jira API tests completed.")

def before_feature(context, feature):
    """
    Runs before each feature.
    """
    print(f"Running feature: {feature.name}")

def after_feature(context, feature):
    """
    Runs after each feature.
    """
    print(f"Completed feature: {feature.name}")

def before_scenario(context, scenario):
    """
    Runs before each scenario.
    """
    print(f"Running scenario: {scenario.name}")
    
    # Reset test data for each scenario
    context.test_data = {}
    
    # Set up mock for API tests if needed
    if 'api' in scenario.tags:
        # We'll set up mocks in the step definitions as needed
        pass

def after_scenario(context, scenario):
    """
    Runs after each scenario.
    """
    print(f"Completed scenario: {scenario.name}")
    
    # Clean up any mocks or patches
    if hasattr(context, 'env_patcher') and context.env_patcher:
        context.env_patcher.stop()
    
    # Stop specific patches
    if hasattr(context, 'requests_patch'):
        context.requests_patch.stop()
    if hasattr(context, 'requests_post_patch'):
        context.requests_post_patch.stop()
    if hasattr(context, 'interface_patch'):
        context.interface_patch.stop()
    
    # Stop all patches to ensure clean state
    patch.stopall() 