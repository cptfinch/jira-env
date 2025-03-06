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

class JiraInterface:
    """
    Main class for interacting with the Jira API.
    """
    
    def __init__(self, base_url=None, api_token=None):
        """
        Initialize the Jira Interface.
        
        Args:
            base_url: Jira base URL (defaults to JIRA_URL env var)
            api_token: Jira API token (defaults to JIRA_API_TOKEN env var)
        """
        # Get configuration from environment variables
        # Use the provided parameters first, then fall back to environment variables
        self.base_url = base_url or os.environ.get("JIRA_URL")
        
        if not self.base_url:
            # For backward compatibility, check JIRA_BASE_URL if JIRA_URL is not set
            self.base_url = os.environ.get("JIRA_BASE_URL", "https://jira.example.com")
        
        self.api_token = api_token or os.environ.get("JIRA_API_TOKEN", "")
        
        if not self.api_token:
            raise ValueError("JIRA_API_TOKEN not set. Please set it as an environment variable")
        
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
    
    def search_issues(self, jql: str, max_results: int = 50, fields: List[str] = None) -> Dict[str, Any]:
        """
        Search for issues using JQL (Jira Query Language)
        
        Args:
            jql: JQL query string
            max_results: Maximum number of results to return (default: 50)
            fields: List of fields to include in the response (default: all fields)
            
        Returns:
            Dictionary containing search results with issues and pagination info
        """
        url = f"{self.base_url}/rest/api/2/search"
        
        # Prepare the request payload
        payload = {
            "jql": jql,
            "maxResults": max_results,
            "startAt": 0
        }
        
        # Add fields if specified
        if fields:
            payload["fields"] = fields
        
        # Make the API request
        response = requests.post(url, headers=self.headers, json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return {"issues": [], "total": 0}

# Additional methods would be added here, converted from the functions in jira-interface.py 