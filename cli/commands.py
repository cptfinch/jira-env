"""
Command-line Interface for Jira Environment

This module provides the command-line interface for searching Jira issues.
"""

import argparse
import json
import sys
import os
import yaml
from typing import Dict, List, Any, Optional

from core import JiraInterface


def load_queries(file_path):
    """Load JQL queries from a YAML file"""
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        return data.get('queries', [])
    except FileNotFoundError:
        print(f"Warning: Query file {file_path} not found")
        return []
    except yaml.YAMLError:
        print(f"Warning: Error parsing YAML file {file_path}")
        return []


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Jira Search Interface")
    
    # Main action argument - only search is supported
    parser.add_argument("action", choices=["search"], help="Action to perform")
    
    # Search-specific arguments
    parser.add_argument("--query", "-q", help="Name of the query to use from jira_queries.yaml")
    parser.add_argument("--jql", "-j", help="Custom JQL query to use instead of a named query")
    parser.add_argument("--format", choices=["json", "table", "summary"], default="summary", 
                        help="Output format (default: summary)")
    parser.add_argument("--limit", "-l", type=int, default=10, help="Maximum number of results to return")
    parser.add_argument("--list-queries", action="store_true", help="List available queries and exit")
    
    return parser.parse_args()


def handle_search(jira, args):
    """Handle the search action"""
    # Display connection information
    masked_token = jira.api_token[:4] + "..." if jira.api_token else "Not set"
    print(f"Connected to: {jira.base_url}")
    print(f"Using API token: {masked_token}")
    print()
    
    # Load queries from YAML file
    queries_file = os.environ.get('JIRA_QUERIES_PATH', os.path.join('data', 'jira_queries.yaml'))
    queries = load_queries(queries_file)
    
    # List available queries if requested
    if args.list_queries:
        print("Available queries:")
        for query in queries:
            print(f"  {query['name']}: {query['description']}")
            print(f"    JQL: {query['jql']}")
            print()
        return None
    
    # Determine which JQL query to use
    jql = None
    if args.jql:
        # Use custom JQL query provided as argument
        jql = args.jql
        print(f"Using custom JQL query: {jql}")
    elif args.query:
        # Find the named query in the loaded queries
        for query in queries:
            if query['name'] == args.query:
                jql = query['jql']
                print(f"Using query '{query['name']}': {query['description']}")
                print(f"JQL: {jql}")
                break
        
        if not jql:
            print(f"Error: Query '{args.query}' not found in {queries_file}")
            return None
    else:
        # No query specified, use the first one as default
        if queries:
            default_query = queries[0]
            jql = default_query['jql']
            print(f"Using default query '{default_query['name']}': {default_query['description']}")
            print(f"JQL: {jql}")
        else:
            print(f"Error: No queries found in {queries_file}")
            return None
    
    # Search for issues using the selected JQL query
    return jira.search_issues(jql, max_results=args.limit)


def format_search_results(results, format_type):
    """Format search results based on the specified format"""
    if not results:
        return "No results found or error occurred"
    
    issues = results.get('issues', [])
    total = results.get('total', 0)
    
    if format_type == "json":
        return json.dumps(results, indent=2)
    
    output = []
    output.append(f"Found {total} issues, showing {len(issues)}:")
    
    for issue in issues:
        key = issue.get('key', 'Unknown')
        summary = issue.get('fields', {}).get('summary', 'No summary')
        status = issue.get('fields', {}).get('status', {}).get('name', 'Unknown')
        
        # Get comments if available
        comments = issue.get('fields', {}).get('comment', {}).get('comments', [])
        recent_comments = comments[-2:] if len(comments) > 0 else []  # Get the last 2 comments
        
        if format_type == "table":
            output.append(f"| {key} | {status} | {summary} |")
            # Add comments in table format
            for comment in recent_comments:
                author = comment.get('author', {}).get('displayName', 'Unknown')
                body = comment.get('body', '').replace('\n', ' ')[:100]  # Truncate long comments
                if len(body) == 100:
                    body += "..."
                output.append(f"|  | Comment by {author} | {body} |")
        else:  # summary
            output.append(f"  {key}: {summary} (Status: {status})")
            # Add comments in summary format
            if recent_comments:
                output.append(f"    Recent comments:")
                for comment in recent_comments:
                    author = comment.get('author', {}).get('displayName', 'Unknown')
                    created = comment.get('created', '').split('T')[0]  # Just get the date part
                    body = comment.get('body', '').replace('\n', ' ')[:100]  # Truncate long comments
                    if len(body) == 100:
                        body += "..."
                    output.append(f"      {created} - {author}: {body}")
    
    if total > len(issues):
        output.append(f"\nShowing {len(issues)} of {total} issues. Use --limit to see more.")
    
    return "\n".join(output)


def main():
    """Main entry point for the CLI"""
    args = parse_args()
    
    try:
        jira = JiraInterface()
        result = handle_search(jira, args)
        if result:
            print(format_search_results(result, args.format))
    
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1) 