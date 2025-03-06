"""
Core Jira Interface Module

This module provides the core functionality for interacting with Jira's REST API,
enabling access to common Jira operations.
"""

import requests
import json
import os
import sys
from typing import Dict, List, Any, Optional, Union
from dotenv import load_dotenv, find_dotenv

# Standard locations for configuration files
DEFAULT_ENV_FILE = ".env"  # Standard .env file in the current directory

class JiraInterface:
    """
    Main class for interacting with the Jira API.
    """
    
    def __init__(self, base_url=None, api_token=None, env_file=None, override=False):
        """
        Initialize the Jira Interface.
        
        Args:
            base_url: Jira base URL (defaults to JIRA_BASE_URL env var)
            api_token: Jira API token (defaults to JIRA_API_TOKEN env var)
            env_file: Path to .env file (defaults to .env in current directory)
            override: Whether to override existing environment variables with values from .env
        """
        # Try to load from .env file if it exists
        if env_file:
            # Load from specified .env file
            load_dotenv(dotenv_path=env_file, override=override)
        else:
            # Auto-discover .env file in current directory or parent directories
            dotenv_path = find_dotenv(usecwd=True)
            if dotenv_path:
                load_dotenv(dotenv_path=dotenv_path, override=override)
        
        # Get configuration from environment variables (possibly set by dotenv)
        self.base_url = base_url or os.environ.get("JIRA_BASE_URL", "https://jira.example.com")
        self.api_token = api_token or os.environ.get("JIRA_API_TOKEN", "")
        
        if not self.api_token:
            raise ValueError("JIRA_API_TOKEN not set. Please set it as an environment variable or in a .env file")
        
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_token}"
        }
    
    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """
        Get information about the authenticated user (equivalent to /rest/api/2/myself)
        
        Returns:
            Dict containing user information or None if request failed
        """
        url = f"{self.base_url}/rest/api/2/myself"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
    
    def get_my_issues(self, max_results=50) -> List[Dict[str, Any]]:
        """
        Get issues assigned to the current user
        
        Args:
            max_results: Maximum number of results to return
            
        Returns:
            List of issues assigned to the current user
        """
        # First get the current user's account ID
        user_info = self.get_current_user()
        if not user_info:
            return []
            
        # Implementation would continue with the rest of the function...
        # For brevity, we're just returning an empty list for now
        return []

# Additional methods would be added here, converted from the functions in jira-interface.py 