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
├── core.py                # Core Jira API functionality
├── cli.py                 # Command-line interface
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

## Configuration

### API Token Setup

1. Generate a Jira API token from your Atlassian account
2. Set the following environment variables:
   ```
   export JIRA_BASE_URL="https://your-jira-instance.atlassian.net"
   export JIRA_API_TOKEN="your-api-token"
   ```
3. Alternatively, create a config file at `~/.config/jira-env/config.env` with the following content:
   ```
   JIRA_BASE_URL=https://your-jira-instance.atlassian.net
   JIRA_API_TOKEN=your-api-token
   ```

## Usage

### Command Line Interface

```bash
# Get information about the current user
jira-interface get-user

# Get issues assigned to the current user
jira-interface get-issues

# Export predefined queries
jira-export
```

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
python -m jira_env.web.interface
```

### Chat Integration

The chat extension provides integration with chat platforms like Slack and Discord.

```python
from jira_env import JiraChatIntegration

# Initialize the chat integration
chat = JiraChatIntegration()

# Send a message with issue information
chat.send_issue_update("PROJ-123")
```

### Interactive Selection

The interactive extension provides a more user-friendly way to select and interact with Jira issues in the terminal.

```python
from jira_env import interactive_issue_selector

# Select an issue interactively
selected_issue = interactive_issue_selector()
print(f"Selected issue: {selected_issue['key']}")
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 