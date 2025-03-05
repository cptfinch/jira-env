# Jira API Interface

A command-line tool for interacting with Jira's REST API, providing easy access to common Jira operations.

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

- Python 3.x
- `requests` library
- Access to a Jira instance with a valid API token

## Setup

1. Clone this repository or download the script
2. Update the configuration in `jira-interface.py`:
   ```python
   JIRA_BASE_URL = "https://your-jira-instance.atlassian.net"
   API_TOKEN = "your-api-token"
   ```
3. Install the required dependencies:
   ```
   pip install requests
   ```

### Using with Nix

If you're using Nix, you can use the provided `flake.nix` to set up a development environment:

```bash
nix develop
```

This will create an environment with Python and all required dependencies.

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

## Extending the Script

The script is designed to be easily extended. To add new functionality:

1. Add a new function to interact with the Jira API
2. Add a new display function if needed
3. Add a new action to the argument parser in the `main()` function
4. Add the corresponding logic to handle the new action

## Troubleshooting

- **Authentication Issues**: Ensure your API token is valid and has the necessary permissions
- **API Errors**: Check the error messages returned by the Jira API for specific issues
- **Rate Limiting**: If you're making many requests, you might hit Jira's rate limits

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests. 