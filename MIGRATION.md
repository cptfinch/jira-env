# Migration Guide

This document provides guidance for migrating from the old project structure to the new package-based structure.

## Overview of Changes

The project has been restructured from a flat script-based approach to a proper Python package structure:

- The main `jira-interface.py` script has been converted to a class-based module in `jira_env/core.py`
- The `jira_export_manager.py` script has been converted to a class-based module in `jira_env/export_manager.py`
- The extension modules have been moved into the `jira_env` package
- Command-line functionality has been moved to `jira_env/cli.py`

## Migration Steps for Users

### Command-line Usage

Old:
```bash
python jira-interface.py get-user
python jira_export_manager.py
```

New:
```bash
# After installing the package
jira-interface get-user
jira-export
```

### Programmatic Usage

Old:
```python
# Importing functions directly from scripts was not supported
```

New:
```python
from jira_env import JiraInterface, JiraExportManager

# Initialize the Jira interface
jira = JiraInterface()

# Get information about the current user
user_info = jira.get_current_user()

# Initialize the export manager
export_manager = JiraExportManager()
export_manager.export_all()
```

### Configuration

The configuration file path has changed:

Old: `~/.config/jira-interface/config.env`
New: `~/.config/jira-env/config.env`

### Extension Modules

The extension modules are now properly integrated into the package:

Old:
```python
# No standard import pattern
```

New:
```python
# RAG extension
from jira_env.rag import JiraRAG

# Web interface
from jira_env.web import JiraWebInterface

# Chat integration
from jira_env.chat import JiraChatIntegration

# Interactive selection
from jira_env.interactive import interactive_issue_selector
```

## Migration Steps for Developers

1. Install the package in development mode:
   ```bash
   cd jira_env
   pip install -e .
   ```

2. Update imports in your code to use the new package structure
3. Update any scripts that call the old scripts directly to use the new entry points
4. Update any configuration paths to use the new paths 