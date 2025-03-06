#!/usr/bin/env python3
# save as jira_export_manager.py

import yaml
import subprocess
import os
import sys
import json
import time
from datetime import datetime

# Enable debug mode
DEBUG = True

def debug(message):
    if DEBUG:
        print(f"DEBUG: {message}")

# Load config
try:
    debug("Loading config from jira_queries.yaml")
    with open('jira_queries.yaml', 'r') as f:
        config = yaml.safe_load(f)
    debug(f"Config loaded successfully: {len(config.get('queries', []))} queries found")
except Exception as e:
    print(f"Error loading config: {e}")
    sys.exit(1)

# Create export directory
today = datetime.now().strftime('%Y-%m-%d')
export_dir = f"jira_exports/{today}"
debug(f"Using export directory: {export_dir}")
os.makedirs(export_dir, exist_ok=True)

# Function to run a query and save the result
def export_query(name, jql, description):
    print(f"Exporting: {name}")
    print(f"Query: {jql}")
    print(f"Description: {description}")
    
    # Run the Jira interface command
    cmd = ['python', 'jira-interface.py', '--action', 'search', '--jql', jql, '--output-format', 'simplified_json', '--max-results', '50']
    debug(f"Running command: {' '.join(cmd)}")
    
    try:
        # Set a timeout for the subprocess
        start_time = time.time()
        debug("Starting subprocess with timeout of 60 seconds")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        elapsed = time.time() - start_time
        debug(f"Subprocess completed in {elapsed:.2f} seconds")
        
        if result.returncode != 0:
            print(f"Error running query: {result.stderr}")
            debug(f"Command failed with return code {result.returncode}")
            debug(f"Stderr: {result.stderr}")
            
            # Try again with a smaller max-results value if the error is related to NoneType
            if "NoneType" in result.stderr:
                debug("Retrying with a smaller max-results value")
                # Modify the command to use a smaller max-results value
                cmd = ['python', 'jira-interface.py', '--action', 'search', '--jql', jql, '--output-format', 'simplified_json', '--max-results', '20']
                debug(f"Retrying command: {' '.join(cmd)}")
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                if result.returncode != 0:
                    debug(f"Retry failed with return code {result.returncode}")
                    return False
            else:
                return False
        
        debug(f"Command succeeded, stdout length: {len(result.stdout)}")
        
        # Check if output is empty
        if not result.stdout.strip():
            print("Error: Empty response from Jira interface")
            debug("Stdout is empty or only whitespace")
            return False
        
        try:
            # Parse the JSON to make sure it's valid
            debug("Parsing JSON response")
            data = json.loads(result.stdout)
            debug(f"JSON parsed successfully, found {len(data.get('issues', []))} issues")
            
            # Add metadata
            data['metadata'] = {
                'name': name,
                'description': description,
                'jql': jql,
                'exported_at': datetime.now().isoformat(),
                'total_issues': data.get('total', 0)
            }
            
            # Save to file
            filename = f"{export_dir}/{name}.json"
            debug(f"Saving to file: {filename}")
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"Saved to: {filename}")
            print(f"Total issues: {data.get('total', 0)}")
            print(f"Issues exported: {len(data.get('issues', []))}")
            print("-" * 50)
            return True
        
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON response: {e}")
            debug(f"JSON decode error: {e}")
            debug(f"First 200 chars of stdout: {result.stdout[:200]}")
            return False
            
    except subprocess.TimeoutExpired:
        print("Error: Command timed out after 60 seconds")
        debug("Subprocess timed out")
        return False
    except Exception as e:
        print(f"Error running command: {e}")
        debug(f"Exception: {e}")
        return False

# Process all queries or specific ones if provided as arguments
queries_to_run = sys.argv[1:] if len(sys.argv) > 1 else [q['name'] for q in config['queries']]
debug(f"Queries to run: {queries_to_run}")

for query_config in config['queries']:
    if query_config['name'] in queries_to_run:
        debug(f"Processing query: {query_config['name']}")
        success = export_query(
            query_config['name'],
            query_config['jql'],
            query_config.get('description', '')
        )
        debug(f"Query {query_config['name']} {'succeeded' if success else 'failed'}")

print(f"Export complete. All files saved to {export_dir}/")

