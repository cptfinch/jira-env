"""
Command-line interface for Jira RAG integration.

This module provides CLI commands for the RAG integration features.
"""

import argparse
import json
import sys
from typing import Dict, Any, Optional

from .core import analyze_issue_with_rag, get_similar_issues, save_issue_resolution

def setup_rag_parser(subparsers):
    """
    Set up the argument parser for RAG-related commands.
    
    Args:
        subparsers: The subparsers object from the main argparse parser
    """
    # analyze-issue command
    analyze_parser = subparsers.add_parser(
        "analyze-issue", 
        help="Analyze an issue using RAG to suggest solutions"
    )
    analyze_parser.add_argument(
        "--issue-key", 
        required=True, 
        help="The key of the issue to analyze"
    )
    analyze_parser.add_argument(
        "--output-format", 
        choices=["text", "json"], 
        default="text",
        help="Output format (text or json)"
    )
    
    # find-similar command
    similar_parser = subparsers.add_parser(
        "find-similar", 
        help="Find issues similar to the given issue"
    )
    similar_parser.add_argument(
        "--issue-key", 
        required=True, 
        help="The key of the issue to find similar issues for"
    )
    similar_parser.add_argument(
        "--top", 
        type=int, 
        default=5,
        help="Maximum number of similar issues to return"
    )
    similar_parser.add_argument(
        "--threshold", 
        type=float, 
        default=0.7,
        help="Minimum similarity score (0-1) for an issue to be considered similar"
    )
    similar_parser.add_argument(
        "--output-format", 
        choices=["text", "json"], 
        default="text",
        help="Output format (text or json)"
    )
    
    # save-resolution command
    save_parser = subparsers.add_parser(
        "save-resolution", 
        help="Save an issue resolution to the knowledge base"
    )
    save_parser.add_argument(
        "--issue-key", 
        required=True, 
        help="The key of the issue that was resolved"
    )
    save_parser.add_argument(
        "--resolution", 
        required=True, 
        help="The resolution that was applied"
    )
    save_parser.add_argument(
        "--feedback", 
        default="",
        help="Optional feedback on the resolution"
    )

def handle_rag_command(args, jira_api):
    """
    Handle RAG-related commands.
    
    Args:
        args: The parsed command-line arguments
        jira_api: The Jira API client
        
    Returns:
        True if a RAG command was handled, False otherwise
    """
    if args.action == "analyze-issue":
        return handle_analyze_issue(args, jira_api)
    elif args.action == "find-similar":
        return handle_find_similar(args, jira_api)
    elif args.action == "save-resolution":
        return handle_save_resolution(args, jira_api)
    
    return False

def handle_analyze_issue(args, jira_api):
    """
    Handle the analyze-issue command.
    
    Args:
        args: The parsed command-line arguments
        jira_api: The Jira API client
        
    Returns:
        True if the command was handled successfully, False otherwise
    """
    # Get the issue from Jira
    issue = jira_api.get_issue(args.issue_key)
    if not issue:
        print(f"Error: Issue {args.issue_key} not found")
        return False
    
    # Analyze the issue
    analysis = analyze_issue_with_rag(issue)
    if not analysis:
        print(f"Error: Failed to analyze issue {args.issue_key}")
        return False
    
    # Output the analysis
    if args.output_format == "json":
        print(json.dumps(analysis, indent=2))
    else:
        print(f"Analysis for issue {args.issue_key}:")
        print(f"\nAnalysis:")
        print(analysis["analysis"])
        
        print(f"\nSuggested Solutions:")
        for i, solution in enumerate(analysis["suggested_solutions"], 1):
            print(f"{i}. {solution}")
        
        if analysis["similar_issues"]:
            print(f"\nSimilar Issues:")
            for issue in analysis["similar_issues"]:
                print(f"- {issue['key']} (Similarity: {issue['similarity']:.2f})")
    
    return True

def handle_find_similar(args, jira_api):
    """
    Handle the find-similar command.
    
    Args:
        args: The parsed command-line arguments
        jira_api: The Jira API client
        
    Returns:
        True if the command was handled successfully, False otherwise
    """
    # Get the issue from Jira
    issue = jira_api.get_issue(args.issue_key)
    if not issue:
        print(f"Error: Issue {args.issue_key} not found")
        return False
    
    # Find similar issues
    similar_issues = get_similar_issues(
        issue, 
        top_n=args.top, 
        similarity_threshold=args.threshold
    )
    
    # Output the similar issues
    if args.output_format == "json":
        print(json.dumps(similar_issues, indent=2))
    else:
        print(f"Issues similar to {args.issue_key}:")
        if not similar_issues:
            print("No similar issues found.")
        else:
            for i, issue in enumerate(similar_issues, 1):
                print(f"{i}. {issue['key']}: {issue.get('fields', {}).get('summary', 'No summary')}")
    
    return True

def handle_save_resolution(args, jira_api):
    """
    Handle the save-resolution command.
    
    Args:
        args: The parsed command-line arguments
        jira_api: The Jira API client
        
    Returns:
        True if the command was handled successfully, False otherwise
    """
    # Get the issue from Jira
    issue = jira_api.get_issue(args.issue_key)
    if not issue:
        print(f"Error: Issue {args.issue_key} not found")
        return False
    
    # Save the resolution
    success = save_issue_resolution(
        issue, 
        args.resolution, 
        args.feedback
    )
    
    if success:
        print(f"Resolution for issue {args.issue_key} saved successfully.")
    else:
        print(f"Error: Failed to save resolution for issue {args.issue_key}")
    
    return success 