# Jira Environment

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

A comprehensive interface to the Jira API, providing easy access to common Jira operations.

## Overview

This Python package provides a comprehensive interface to the Jira API, allowing you to perform most common Jira operations from the command line or programmatically. It's designed to be easy to use and can be integrated into your workflow or automation scripts.

## Features

- Core API functionality for common Jira operations
- Export management for Jira queries
- Extensions for RAG, web interface, chat integration, and interactive selection

## Project Structure

The project follows a modular architecture with the following components:

```
project/
├── core/                  # Core Jira API functionality
│   ├── __init__.py        # Module exports
│   └── interface.py       # JiraInterface implementation
├── cli/                   # Command-line interface
│   ├── __init__.py        # Module exports
│   ├── commands.py        # CLI commands implementation
│   └── jira.py            # CLI entry point
├── jira-cli.py            # Executable CLI script
├── exports/               # Export functionality extension
│   ├── manager.py         # Export manager implementation
│   └── queries/           # Query definitions
├── rag/                   # RAG extension
├── web/                   # Web interface extension
├── chat/                  # Chat integration extension
└── interactive/           # Interactive selection extension
```

Each extension is a self-contained module with its own implementation and dependencies.

## Installation

### From Source

```bash
git clone https://github.com/cptfinch/jira-env.git
cd jira-env
pip install -e .
```

### Using pip

```bash
pip install jira-env
```

### Using Nix

If you use the Nix package manager, you can install and use jira-env with Nix:

```bash
# Clone the repository
git clone https://github.com/cptfinch/jira-env.git
cd jira-env

# Enter a development shell
nix develop

# Or install the package
nix profile install .
```

### Using home-manager

If you use home-manager, you can add jira-env to your configuration:

```nix
{
  inputs.jira-env.url = "github:cptfinch/jira-env";
  
  outputs = { self, nixpkgs, home-manager, jira-env, ... }: {
    homeConfigurations."your-username" = home-manager.lib.homeManagerConfiguration {
      # ... your other configuration ...
      
      modules = [
        jira-env.homeManagerModule
        
        {
          programs.jira-env = {
            enable = true;
            baseUrl = "https://your-jira-instance.atlassian.net";
            
            # Optional: API token (not recommended, use environment variable instead)
            # apiToken = "your-api-token";
            
            # Optional: Enable specific extensions
            enableExtensions = [ "web" "interactive" ];
          };
        }
      ];
    };
  };
}
```

## Configuration

### API Token Setup

You have two options for configuring your Jira credentials:

#### Option 1: Environment Variables

Set the following environment variables in your system:

```bash
export JIRA_BASE_URL="https://your-jira-instance.atlassian.net"
# OR
export JIRA_URL="https://your-jira-instance.atlassian.net"
export JIRA_API_TOKEN="your-api-token"
```

The system supports both `JIRA_BASE_URL` and `JIRA_URL` environment variables for the Jira instance URL. If both are set, `JIRA_BASE_URL` takes precedence.

This is the recommended approach for production environments or when using tools like SOPS for secret management.

#### Option 2: Using a .env File

Create a `.env` file in your project directory with the following content:

```
JIRA_BASE_URL=https://your-jira-instance.atlassian.net
# OR
JIRA_URL=https://your-jira-instance.atlassian.net
JIRA_API_TOKEN=your-api-token
```

The `.env` file will be automatically detected and loaded when you use the JiraInterface.

> **Note**: Make sure to add `.env` to your `.gitignore` file to avoid committing sensitive information to version control.

You can also specify a custom location for your .env file:

```python
from jira_env import JiraInterface

# Load from a custom .env file location
jira = JiraInterface(env_file="/path/to/your/.env")
```

## Usage

### Command Line Interface

```bash
# Get information about the current user
./jira-cli.py get-user

# Get issues assigned to the current user
./jira-cli.py get-issues

# Export predefined queries
./jira-cli.py export

# Search for issues using predefined queries
./jira-cli.py search --query all_my_issues

# Search with a custom JQL query
./jira-cli.py search --jql "assignee = currentUser() AND updated >= -1d"

# List all available predefined queries
./jira-cli.py search --list-queries

# Limit the number of results
./jira-cli.py search --query recent_updates --limit 5

# Output in different formats (summary, json, table)
./jira-cli.py search --query high_priority --format json
```

### Search Results with Comments

The search results include recent comments for each issue, providing more context about the current status and activity:

```
NCIPT-42861: SBF.128 - ukhspc is sending PLC data from the future (Status: Work in progress)
  Recent comments:
    2025-01-08 - Christopher Finch: Resolving this one to consolidate actions in to PSD-6147...
    2025-01-21 - Frederic Moniquet: (CCB - CDANTIN,FMONIQU) Reopening as the issue is not solved...
```

- The two most recent comments are displayed for each issue
- Comments include the date, author, and a truncated version of the content
- Long comments are truncated to keep the output readable
- Comments are formatted differently in each output format:
  - In summary format: Indented under each issue
  - In table format: Shown as additional rows
  - In JSON format: Full comment data is included

This feature helps you quickly understand the current status and recent activity on issues without having to open them in the Jira web interface.

### Search Command Examples

The `search` command provides powerful functionality for finding Jira issues. Here are some examples:

#### Using Predefined Queries

```bash
# Search for all your unresolved issues
./jira-cli.py search --query all_my_issues

# Search for your unresolved issues in a specific project
./jira-cli.py search --query crpt_issues

# Search for your high priority unresolved issues
./jira-cli.py search --query high_priority

# Search for your issues updated in the last week
./jira-cli.py search --query recent_updates
```

#### Using Custom JQL Queries

```bash
# Search for issues updated in the last day
./jira-cli.py search --jql "assignee = currentUser() AND updated >= -1d"

# Search for issues in a specific project
./jira-cli.py search --jql "project = PROJ AND statusCategory != Done"

# Search for issues with a specific label
./jira-cli.py search --jql "labels = important AND assignee = currentUser()"

# Search for issues due in the next week
./jira-cli.py search --jql "duedate >= now() AND duedate <= 1w"
```

#### Controlling Output

```bash
# Limit the number of results
./jira-cli.py search --query all_my_issues --limit 5

# Output in JSON format for programmatic processing
./jira-cli.py search --query recent_updates --format json

# Output in table format for better readability
./jira-cli.py search --query high_priority --format table

# View issues with their recent comments
./jira-cli.py search --query all_my_issues --limit 5
```

### Predefined Queries

The system comes with several predefined queries in `exports/queries/jira_queries.yaml`:

- **all_my_issues**: All your unresolved issues across all projects
  - JQL: `assignee = currentUser() AND statusCategory != Done`

- **crpt_issues**: Your unresolved issues in the CRPT project
  - JQL: `assignee = currentUser() AND statusCategory != Done AND project = CRPT`

- **high_priority**: Your high priority unresolved issues
  - JQL: `assignee = currentUser() AND priority = High AND statusCategory != Done`

- **recent_updates**: Your issues updated in the last week
  - JQL: `assignee = currentUser() AND updated >= -7d`

### Creating Custom Queries

You can add your own predefined queries by editing the `exports/queries/jira_queries.yaml` file:

```yaml
queries:
  - name: my_custom_query
    jql: "project = MYPROJ AND assignee = currentUser() AND labels = important"
    description: "My important issues in MYPROJ"
```

After adding your custom query, you can use it with:

```bash
./jira-cli.py search --query my_custom_query
```

### JQL Reference

JQL (Jira Query Language) is a powerful query language for searching Jira issues. Here are some common JQL operators and examples:

- **Basic operators**: `=`, `!=`, `>`, `>=`, `<`, `<=`, `IN`, `NOT IN`, `~` (contains), `!~` (does not contain)
- **Logical operators**: `AND`, `OR`, `NOT`
- **Special functions**: `currentUser()`, `now()`, `empty()`, `membersOf()`
- **Time expressions**: `-1d` (1 day ago), `1w` (1 week from now), `startOfDay()`, `endOfDay()`

Examples:

```
project = PROJ AND status = "In Progress"
assignee = currentUser() AND priority IN (High, Highest)
labels ~ "important" AND updated >= -7d
duedate <= 1w OR duedate IS EMPTY
```

For more information on JQL, refer to the [Atlassian JQL documentation](https://support.atlassian.com/jira-software-cloud/docs/advanced-search-reference-jql-fields/).

### Programmatic Usage

```python
from jira_env import JiraInterface

# Initialize the Jira interface
jira = JiraInterface()

# Get information about the current user
user_info = jira.get_current_user()
print(user_info)

# Get issues assigned to the current user
my_issues = jira.get_my_issues()
for issue in my_issues:
    print(f"{issue['key']}: {issue['summary']}")
```

### Using the Export Manager

```python
from jira_env import JiraExportManager

# Initialize the export manager
export_manager = JiraExportManager()

# Export all predefined queries
exported_files = export_manager.export_all()
print(f"Exported {len(exported_files)} files")

# Export a specific query
export_manager.export_query(
    name="high_priority",
    jql="assignee = currentUser() AND priority = High AND statusCategory != Done",
    description="My high priority unresolved issues"
)
```

### Using with Nix

When using the Nix development shell, you can run the commands directly:

```bash
# Enter the development shell
nix develop

# Run the CLI
./jira-cli.py --help

# Run the export manager
python -m exports.manager

# Run the web interface (development mode)
python -m web.interface
```

Note: Some modules like the web interface expect the package to be installed as 'jira_env'. 
In development mode, you may need to run the Python files directly instead of using the module syntax.

## Extensions

### RAG Integration

The RAG (Retrieval-Augmented Generation) extension provides intelligent analysis of Jira issues.

```python
from jira_env import JiraRAG

# Initialize the RAG system
rag = JiraRAG()

# Analyze issues
analysis = rag.analyze_issues(["PROJ-123", "PROJ-456"])
print(analysis)
```

### Web Interface

The web extension provides a browser-based interface to the Jira API.

```bash
# Start the web interface
python -m web.interface
```

### Chat Integration

The chat integration provides integration with chat platforms like Slack and Discord.

```python
from jira_env import JiraChatIntegration

# Initialize the chat integration
chat = JiraChatIntegration()

# Send a message about an issue
chat.send_issue_update("PROJ-123", "Issue has been resolved")
```

### Interactive Selection

The interactive extension provides a terminal-based UI for selecting and working with Jira issues.

```python
from jira_env import interactive_issue_selector

# Select an issue interactively
selected_issue = interactive_issue_selector()
print(f"You selected: {selected_issue['key']}")

# Or use batch selection
from jira_env import batch_issue_selector

selected_issues = batch_issue_selector()
print(f"You selected {len(selected_issues)} issues")
```

## Development

### Module Structure

The project is organized into several modules:

1. **core**: Contains the core JiraInterface class for interacting with the Jira API
2. **cli**: Contains the command-line interface implementation
3. **exports**: Handles exporting Jira queries to various formats
4. **rag**: Implements Retrieval-Augmented Generation for Jira issues
5. **web**: Provides a web interface to the Jira API
6. **chat**: Implements chat platform integrations
7. **interactive**: Provides terminal-based interactive selection tools

### Adding New Features

To add a new feature:

1. Identify which module it belongs to
2. Implement the feature in the appropriate module
3. Update the module's `__init__.py` to export any new public functions or classes
4. Update the top-level `__init__.py` if the feature should be part of the public API
5. Add tests for the new feature
6. Update documentation

### Running Tests

```bash
# Run all tests
pytest

# Run tests for a specific module
pytest tests/test_core.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 