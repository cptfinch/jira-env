"""
Jira Web Interface Module

This package provides a web interface for the Jira API Interface,
allowing users to interact with Jira through a browser-based UI.
"""

__version__ = "0.1.0-alpha"

from jira_env.web.interface import (
    JiraWebInterface,
    streamlit_app_example,
    main
)

__all__ = [
    'JiraWebInterface',
    'streamlit_app_example',
    'main'
] 