@connection @api
Feature: Jira Connection
  As a developer
  I want to connect to Jira API
  So that I can interact with Jira issues

  Background:
    Given the Jira API is mocked

  @initialization @custom_params
  Scenario: Initialize Jira interface with custom parameters
    Given I have custom Jira connection parameters
    When I create a JiraInterface with these parameters
    Then the instance should use the custom parameters

  @user_info @success
  Scenario: Get current user information
    Given I have a valid Jira connection
    When I request the current user information
    Then I should receive the user details

  @user_info @error @authentication
  Scenario: Handle authentication errors
    Given I have an invalid API token
    When I request the current user information
    Then I should receive an error response 