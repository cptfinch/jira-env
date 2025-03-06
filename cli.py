"""
Command-line Interface for Jira Environment

This module provides the command-line interface for interacting with the Jira API.
"""

import argparse
import json
import sys
from typing import Dict, List, Any, Optional

from core import JiraInterface


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Jira API Interface")
    
    # Main action argument
    parser.add_argument("action", choices=[
        "get-user", "get-issues", "get-issue", "create-issue", "update-issue",
        "add-comment", "get-projects", "get-boards", "get-sprints", "transition-issue"
    ], help="Action to perform")
    
    # Common arguments
    parser.add_argument("--issue-key", help="Jira issue key (e.g., PROJ-123)")
    parser.add_argument("--project", help="Jira project key")
    parser.add_argument("--board-id", help="Jira board ID")
    parser.add_argument("--format", choices=["json", "table", "summary"], default="summary", 
                        help="Output format (default: summary)")
    
    # Other arguments would be added here...
    
    return parser.parse_args()


def main():
    """Main entry point for the CLI"""
    args = parse_args()
    
    try:
        jira = JiraInterface()
        
        # Handle different actions
        if args.action == "get-user":
            result = jira.get_current_user()
        elif args.action == "get-issues":
            result = jira.get_my_issues()
        # Other actions would be handled here...
        else:
            print(f"Action {args.action} not implemented")
            sys.exit(1)
        
        # Format and display results
        if args.format == "json":
            print(json.dumps(result, indent=2))
        elif args.format == "table":
            # Table formatting would be implemented here
            print("Table formatting not implemented yet")
        else:  # summary
            # Summary formatting would be implemented here
            print("Summary of results:")
            print(f"Found {len(result) if isinstance(result, list) else 1} items")
    
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main() 