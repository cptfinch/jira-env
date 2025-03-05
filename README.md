# Jira API Interface

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

A command-line tool for interacting with Jira's REST API, providing easy access to common Jira operations.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Standard Installation](#standard-installation)
  - [Using with Nix](#using-with-nix)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Basic Usage](#basic-usage)
  - [Available Actions](#available-actions)
  - [Common Parameters](#common-parameters)
- [Examples](#examples)
- [Workflow Examples](#workflow-examples)
  - [Daily Task Management](#daily-task-management)
  - [Sprint Planning](#sprint-planning)
- [Extending the Script](#extending-the-script)
  - [Example: Adding a New API Function](#example-adding-a-new-api-function)
- [Troubleshooting](#troubleshooting)
  - [Authentication Issues](#authentication-issues)
  - [API Errors](#api-errors)
  - [Common Error Messages](#common-error-messages)
- [License](#license)
- [Contributing](#contributing)
  - [Code Style](#code-style)
- [Acknowledgements](#acknowledgements)

## Overview

This Python script provides a comprehensive interface to the Jira API, allowing you to perform most common Jira operations from the command line. It's designed to be easy to use and can be integrated into your workflow or automation scripts.

## Features

- **User Information**: Get details about the current authenticated user
- **Issue Management**: 
  - Get issues assigned to you
  - Get your unresolved issues
  - Search for issues using JQL queries
  - Create new issues
  - Update existing issues
  - Add comments to issues
  - Transition issues between statuses
- **Project Information**:
  - List all accessible projects
  - Get detailed information about specific projects
- **Agile Boards & Sprints**:
  - List all accessible boards
  - Get board details
  - List sprints for a board
  - Get issues in a sprint
- **Saved Filters**:
  - List your saved filters (custom searches)
  - Get details of specific filters
  - Search for issues using saved filters

## Prerequisites

- Python 3.6 or higher
- `requests` library
- Access to a Jira instance with a valid API token

## Installation

### Standard Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/cptfinch/jira-env.git
   cd jira-env
   ```

2. Install the required dependencies:
   ```bash
   pip install requests
   ```

### Using with Nix

If you're using Nix, you can use the provided `flake.nix` to set up a development environment:

```bash
nix develop
```

This will create an environment with Python and all required dependencies.

## Configuration

Before using the tool, you need to configure your Jira credentials:

1. Update the configuration in `jira-interface.py`:
   ```python
   JIRA_BASE_URL = "https://your-jira-instance.atlassian.net"
   API_TOKEN = "your-api-token"
   ```

2. Alternatively, you can set environment variables:
   ```bash
   export JIRA_BASE_URL="https://your-jira-instance.atlassian.net"
   export JIRA_API_TOKEN="your-api-token"
   ```

> **Security Note**: It's recommended to use environment variables rather than hardcoding your API token in the script.

## Usage

The script uses a command-line interface with various actions and parameters.

### Basic Usage

```bash
python jira-interface.py --action <action> [parameters]
```

### Available Actions

1. **user**: Get information about the current user
   ```bash
   python jira-interface.py --action user
   ```

2. **my-issues**: Get issues assigned to the current user
   ```bash
   python jira-interface.py --action my-issues --max-results 10
   ```

3. **my-unresolved-issues**: Get unresolved issues assigned to you
   ```bash
   python jira-interface.py --action my-unresolved-issues --max-results 10
   ```

4. **search**: Search for issues using a JQL query
   ```bash
   python jira-interface.py --action search --jql "project = PROJ AND status = Open"
   ```

5. **create**: Create a new issue
   ```bash
   python jira-interface.py --action create --project PROJ --summary "Issue summary" --description "Issue description" --issue-type "Task" --priority "Medium"
   ```

6. **update**: Update an existing issue
   ```bash
   python jira-interface.py --action update --issue-key PROJ-123 --new-summary "Updated summary" --new-description "Updated description" --new-priority "High"
   ```

7. **comment**: Add a comment to an issue
   ```bash
   python jira-interface.py --action comment --issue-key PROJ-123 --comment "This is a comment"
   ```

8. **transition**: Change the status of an issue
   ```bash
   python jira-interface.py --action transition --issue-key PROJ-123 --transition "In Progress"
   ```

9. **projects**: List all projects
   ```bash
   python jira-interface.py --action projects
   ```

10. **project-details**: Get detailed information about a project
    ```bash
    python jira-interface.py --action project-details --project PROJ
    ```

11. **boards**: List all Agile boards
    ```bash
    python jira-interface.py --action boards
    ```

12. **board-details**: Get detailed information about a board
    ```bash
    python jira-interface.py --action board-details --board-id 123
    ```

13. **sprints**: List sprints for a board
    ```bash
    python jira-interface.py --action sprints --board-id 123 --sprint-state active
    ```

14. **sprint-issues**: Get issues in a sprint
    ```bash
    python jira-interface.py --action sprint-issues --board-id 123 --sprint-id 456
    ```

15. **filters**: List your saved filters (custom searches)
    ```bash
    python jira-interface.py --action filters
    ```

16. **filter-details**: Get details of a specific filter
    ```bash
    python jira-interface.py --action filter-details --filter-id 123
    ```

17. **search-with-filter**: Search for issues using a saved filter
    ```bash
    python jira-interface.py --action search-with-filter --filter-id 123
    ```

### Common Parameters

- `--max-results`: Maximum number of results to return (default: 10)
- `--jql`: JQL query for searching issues
- `--project`: Project key for creating issues or getting project details
- `--issue-key`: Issue key for update/comment/transition actions (e.g., PROJ-123)
- `--board-id`: Board ID for board-details, sprints, and sprint-issues actions
- `--sprint-id`: Sprint ID for sprint-issues action
- `--sprint-state`: Sprint state filter for sprints action (active, future, closed)
- `--filter-id`: Filter ID for filter-details and search-with-filter actions

For a complete list of parameters, run:
```bash
python jira-interface.py --help
```

## Examples

### Get your assigned issues

```bash
python jira-interface.py --action my-issues
```

### Get your unresolved issues

```bash
python jira-interface.py --action my-unresolved-issues
```

### Search for high-priority open issues in a project

```bash
python jira-interface.py --action search --jql "project = PROJ AND priority = High AND status = Open"
```

### Create a bug report

```bash
python jira-interface.py --action create --project PROJ --summary "Bug: Application crashes on startup" --description "The application crashes immediately when launched on Windows 10" --issue-type "Bug" --priority "High"
```

### Mark an issue as "In Progress"

```bash
python jira-interface.py --action transition --issue-key PROJ-123 --transition "In Progress"
```

### Get active sprints for a board

```bash
python jira-interface.py --action sprints --board-id 123 --sprint-state active
```

### Use a saved filter to find your unresolved issues

```bash
# First, list your saved filters
python jira-interface.py --action filters

# Then use a specific filter by its ID
python jira-interface.py --action search-with-filter --filter-id 123
```

## Workflow Examples

### Daily Task Management

```bash
# Start your day by checking your unresolved issues
python jira-interface.py --action my-unresolved-issues

# Pick an issue to work on and mark it as "In Progress"
python jira-interface.py --action transition --issue-key PROJ-123 --transition "In Progress"

# Add a comment about what you're working on
python jira-interface.py --action comment --issue-key PROJ-123 --comment "Working on fixing the database connection issue"

# When finished, mark the issue as "Done"
python jira-interface.py --action transition --issue-key PROJ-123 --transition "Done"
```

### Sprint Planning

```bash
# List all active sprints for your team's board
python jira-interface.py --action sprints --board-id 123 --sprint-state active

# View issues in the current sprint
python jira-interface.py --action sprint-issues --board-id 123 --sprint-id 456

# Create a new task for the sprint
python jira-interface.py --action create --project PROJ --summary "Implement login feature" --description "Add user authentication to the application" --issue-type "Task" --priority "Medium"
```

## Extending the Script

The script is designed to be easily extended. To add new functionality:

1. Add a new function to interact with the Jira API
2. Add a new display function if needed
3. Add a new action to the argument parser in the `main()` function
4. Add the corresponding logic to handle the new action

### Example: Adding a New API Function

```python
def get_issue_watchers(issue_key):
    """Get the list of watchers for an issue."""
    url = f"{JIRA_BASE_URL}/rest/api/2/issue/{issue_key}/watchers"
    response = make_request("GET", url)
    return response.json()

def display_watchers(watchers_data):
    """Display the watchers of an issue."""
    print(f"Watchers ({watchers_data['watchCount']}):")
    for watcher in watchers_data['watchers']:
        print(f"- {watcher['displayName']} ({watcher['name']})")

# Then in the main() function:
# Add a new action to the argument parser
parser.add_argument("--action", choices=[..., "watchers"], help="Action to perform")

# Add the logic to handle the new action
if args.action == "watchers":
    if not args.issue_key:
        print("Error: --issue-key is required for the watchers action")
        sys.exit(1)
    watchers_data = get_issue_watchers(args.issue_key)
    display_watchers(watchers_data)
```

## Troubleshooting

### Authentication Issues

- **Invalid API Token**: Ensure your API token is valid and has not expired
- **Insufficient Permissions**: Verify that your Jira account has the necessary permissions for the actions you're trying to perform
- **Environment Variables**: If using environment variables, ensure they are correctly set and accessible to the script

### API Errors

- **Rate Limiting**: If you receive 429 errors, you might be hitting Jira's rate limits. Add delays between requests or reduce the frequency of calls
- **Invalid JQL**: If your searches fail, check your JQL syntax for errors
- **Missing Fields**: When creating or updating issues, ensure all required fields for your Jira configuration are provided

### Common Error Messages

- **"Issue does not exist or you do not have permission to see it"**: Check the issue key and your permissions
- **"Field 'XXX' cannot be set"**: This field might be read-only or require a specific format
- **"Transition 'XXX' is not valid"**: The transition name might be incorrect or not available for the current issue status

## License

This project is open source and available under the [MIT License](https://opensource.org/licenses/MIT).

## Contributing

Contributions are welcome! Here's how you can contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

### Code Style

Please follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for Python code.

## Acknowledgements

- [Jira REST API Documentation](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/)
- [Python Requests Library](https://requests.readthedocs.io/) 