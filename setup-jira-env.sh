#!/bin/bash

# Script to set up environment variables for jira-interface
# Source this file in your shell: source setup-jira-env.sh

# Set your Jira API token here
export JIRA_API_TOKEN="your-api-token-here"

# Set your Jira base URL (this should match the one in your home-manager config)
export JIRA_BASE_URL="https://your-jira-instance.atlassian.net"

echo "Jira environment variables set:"
echo "JIRA_BASE_URL=$JIRA_BASE_URL"
echo "JIRA_API_TOKEN=********" # Don't print the actual token for security

# You can now use jira-interface commands
echo "You can now use jira-interface commands, for example:"
echo "jira-interface --action my-issues" 