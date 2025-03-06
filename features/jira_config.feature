Feature: Jira Configuration
  As a developer
  I want to ensure my Jira configuration is correct
  So that I can connect to the Jira API

  Scenario: Verify base URL is set correctly
    Given I have set the JIRA_BASE_URL environment variable to "https://jira.goiba.net"
    When I create a JiraInterface instance for config testing
    Then the instance should use "https://jira.goiba.net" as the base URL

  Scenario: Verify API token is set correctly
    Given I have set the JIRA_API_TOKEN environment variable
    When I create a JiraInterface instance for config testing
    Then the instance should have a valid API token

  Scenario: Test connection to Jira
    Given I have set both JIRA_BASE_URL and JIRA_API_TOKEN environment variables
    When I request the current user information for config testing
    Then I should receive a successful response with user details 