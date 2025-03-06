"""
Jira Interactive Selection Module

This package provides interactive terminal interfaces for the Jira API Interface,
enabling more user-friendly selection and interaction with Jira issues.
"""

__version__ = "0.1.0-alpha"

from jira_env.interactive.selection import (
    interactive_issue_selector,
    batch_issue_selector,
    interactive_query_builder,
    get_issues_interactive
)

__all__ = [
    'interactive_issue_selector',
    'batch_issue_selector',
    'interactive_query_builder',
    'get_issues_interactive'
] 