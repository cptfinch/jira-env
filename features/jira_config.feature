@config @api
Feature: Jira Configuration
  As a developer
  I want to ensure my Jira configuration is correct
  So that I can connect to the Jira API

  Background:
    # Common setup for all scenarios
    Given the Jira API is mocked

  @base_url @validation
  Scenario: Verify base URL is set correctly
    Given I have configured the Jira base URL as "https://jira.goiba.net"
    When I create a JiraInterface instance for config testing
    Then the instance should use "https://jira.goiba.net" as the base URL

  @api_token @validation
  Scenario: Verify API token is set correctly
    Given I have configured a valid Jira API token
    When I create a JiraInterface instance for config testing
    Then the instance should have a valid API token

  @connection @validation
  Scenario: Test connection to Jira
    Given I have configured Jira connection parameters
    When I request the current user information for config testing
    Then I should receive a successful response with user details 