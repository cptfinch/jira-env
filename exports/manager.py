"""
Jira Export Manager Module

This module provides functionality for exporting Jira queries to files.
"""

import yaml
import os
import sys
import json
import time
import subprocess
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

from core import JiraInterface


class JiraExportManager:
    """
    Manager for exporting Jira queries to files.
    """
    
    def __init__(self, config_file=None, export_dir=None, debug=False):
        """
        Initialize the Jira Export Manager.
        
        Args:
            config_file: Path to the YAML config file (defaults to exports/queries/jira_queries.yaml)
            export_dir: Directory to export to (defaults to jira_exports/{today})
            debug: Whether to enable debug output
        """
        self.debug_mode = debug
        self.config_file = config_file or 'exports/queries/jira_queries.yaml'
        self.jira = JiraInterface()
        
        # Load config
        try:
            self.debug(f"Loading config from {self.config_file}")
            with open(self.config_file, 'r') as f:
                self.config = yaml.safe_load(f)
            self.debug(f"Config loaded successfully: {len(self.config.get('queries', []))} queries found")
        except Exception as e:
            print(f"Error loading config: {e}")
            raise
        
        # Create export directory
        today = datetime.now().strftime('%Y-%m-%d')
        self.export_dir = export_dir or f"jira_exports/{today}"
        self.debug(f"Using export directory: {self.export_dir}")
        os.makedirs(self.export_dir, exist_ok=True)
    
    def debug(self, message):
        """Print debug message if debug mode is enabled"""
        if self.debug_mode:
            print(f"DEBUG: {message}")
    
    def export_query(self, name, jql, description):
        """
        Export a single query to a file.
        
        Args:
            name: Name of the query
            jql: JQL query string
            description: Description of the query
        
        Returns:
            Path to the exported file
        """
        print(f"Exporting: {name}")
        print(f"Query: {jql}")
        print(f"Description: {description}")
        
        # Use the JiraInterface directly instead of subprocess
        try:
            self.debug(f"Executing JQL query: {jql}")
            start_time = time.time()
            
            # This would call the appropriate method in JiraInterface
            # For now, we'll just create a placeholder
            # result = self.jira.search_issues(jql, max_results=50)
            result = {"issues": []}  # Placeholder
            
            elapsed = time.time() - start_time
            self.debug(f"Query completed in {elapsed:.2f} seconds")
            
            # Save to file
            output_file = os.path.join(self.export_dir, f"{name}.json")
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)
            
            print(f"Exported to {output_file}")
            return output_file
            
        except Exception as e:
            print(f"Error exporting query {name}: {e}")
            return None
    
    def export_all(self):
        """
        Export all queries defined in the config file.
        
        Returns:
            List of paths to exported files
        """
        exported_files = []
        
        for query in self.config.get('queries', []):
            name = query.get('name')
            jql = query.get('jql')
            description = query.get('description', '')
            
            if name and jql:
                result = self.export_query(name, jql, description)
                if result:
                    exported_files.append(result)
            else:
                print(f"Skipping invalid query: {query}")
        
        return exported_files


def main():
    """Command-line entry point"""
    try:
        manager = JiraExportManager(debug=True)
        exported_files = manager.export_all()
        print(f"Exported {len(exported_files)} files")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 