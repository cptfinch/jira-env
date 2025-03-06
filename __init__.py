"""
Jira Environment - A comprehensive interface to the Jira API

This package provides tools for interacting with Jira's REST API, including:
- Core API functionality for common Jira operations
- Export management for Jira queries
- Extensions for RAG, web interface, chat integration, and interactive selection
"""

__version__ = "0.1.0"

# Import core functionality
from core import JiraInterface

# Import CLI functionality
from cli import main, parse_args

# Import extension modules
from rag import JiraRAG
from web import JiraWebInterface
from chat import JiraChatIntegration
from interactive import interactive_issue_selector, batch_issue_selector, get_issues_interactive

__all__ = [
    # Core
    'JiraInterface',
    
    # CLI
    'main',
    'parse_args',
    
    # RAG
    'JiraRAG',
    
    # Web
    'JiraWebInterface',
    
    # Chat
    'JiraChatIntegration',
    
    # Interactive
    'interactive_issue_selector',
    'batch_issue_selector',
    'get_issues_interactive',
] 