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

## Extensions

### RAG Integration

The RAG (Retrieval-Augmented Generation) extension provides intelligent analysis of Jira issues.

```python
from jira_env.rag import JiraRAG

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

### Interactive Selection

The interactive extension provides a more user-friendly way to select and interact with Jira issues in the terminal.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 