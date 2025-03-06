#!/usr/bin/env python3
"""
Demo script for searching Jira issues using the JiraInterface class
and JQL queries from the jira_queries.yaml file.
"""

import os
import yaml
import argparse
from core import JiraInterface

def load_queries(file_path):
    """Load JQL queries from a YAML file"""
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data.get('queries', [])

def main():
    """Main function to demonstrate Jira issue search"""
    parser = argparse.ArgumentParser(description='Search Jira issues using JQL queries')
    parser.add_argument('--query', '-q', help='Name of the query to use from jira_queries.yaml')
    parser.add_argument('--jql', '-j', help='Custom JQL query to use instead of a named query')
    parser.add_argument('--limit', '-l', type=int, default=10, help='Maximum number of results to return')
    parser.add_argument('--list-queries', action='store_true', help='List available queries and exit')
    args = parser.parse_args()
    
    # Load queries from YAML file
    queries_file = os.path.join('exports', 'queries', 'jira_queries.yaml')
    queries = load_queries(queries_file)
    
    # List available queries if requested
    if args.list_queries:
        print("Available queries:")
        for query in queries:
            print(f"  {query['name']}: {query['description']}")
            print(f"    JQL: {query['jql']}")
            print()
        return
    
    # Initialize Jira interface
    try:
        jira = JiraInterface()
    except ValueError as e:
        print(f"Error: {e}")
        print("Make sure you have set JIRA_API_TOKEN in your .env file")
        return
    
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
            return
    else:
        # No query specified, use the first one as default
        if queries:
            default_query = queries[0]
            jql = default_query['jql']
            print(f"Using default query '{default_query['name']}': {default_query['description']}")
            print(f"JQL: {jql}")
        else:
            print(f"Error: No queries found in {queries_file}")
            return
    
    # Search for issues using the selected JQL query
    results = jira.search_issues(jql, max_results=args.limit)
    
    # Display results
    issues = results.get('issues', [])
    total = results.get('total', 0)
    
    print(f"\nFound {total} issues, showing {len(issues)}:")
    for issue in issues:
        key = issue.get('key', 'Unknown')
        summary = issue.get('fields', {}).get('summary', 'No summary')
        status = issue.get('fields', {}).get('status', {}).get('name', 'Unknown')
        print(f"  {key}: {summary} (Status: {status})")
    
    if total > len(issues):
        print(f"\nShowing {len(issues)} of {total} issues. Use --limit to see more.")

if __name__ == "__main__":
    main() 