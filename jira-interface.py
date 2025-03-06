import requests
import json
import argparse
import os
import sys

# Jira API configuration
JIRA_BASE_URL = os.environ.get("JIRA_BASE_URL", "https://jira.example.com")
API_TOKEN = os.environ.get("JIRA_API_TOKEN", "")

if not API_TOKEN:
    # Try to load from config file if environment variable is not set
    config_path = os.path.expanduser("~/.config/jira-interface/config.env")
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            for line in f:
                if line.strip() and '=' in line:
                    key, value = line.strip().split('=', 1)
                    if key == "JIRA_API_TOKEN":
                        API_TOKEN = value.strip('"\'')
                    elif key == "JIRA_BASE_URL":
                        JIRA_BASE_URL = value.strip('"\'')

if not API_TOKEN:
    print("Error: JIRA_API_TOKEN not set. Please set it as an environment variable or in ~/.config/jira-interface/config.env")
    sys.exit(1)

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_TOKEN}"
}

def get_current_user():
    """Get information about the authenticated user (equivalent to /rest/api/2/myself)"""
    url = f"{JIRA_BASE_URL}/rest/api/2/myself"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def get_my_issues(max_results=50):
    """Get issues assigned to the current user"""
    # First get the current user's account ID
    user_info = get_current_user()
    if not user_info:
        print("Could not determine current user")
        return None
    
    # JQL query to find issues assigned to the current user
    jql_query = f"assignee = currentUser() ORDER BY updated DESC"
    
    url = f"{JIRA_BASE_URL}/rest/api/2/search"
    params = {
        "jql": jql_query,
        "maxResults": max_results
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def get_my_unresolved_issues(max_results=50):
    """Get unresolved issues assigned to the current user (equivalent to 'My not done issues' filter)"""
    # JQL query from your saved filter
    jql_query = "assignee = currentUser() AND statusCategory != Done ORDER BY created ASC"
    
    return search_issues(jql_query, max_results)

def get_saved_filters(max_results=50):
    """Get saved filters (custom searches) for the current user"""
    url = f"{JIRA_BASE_URL}/rest/api/2/filter/favourite"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def get_filter_details(filter_id):
    """Get details of a specific saved filter"""
    url = f"{JIRA_BASE_URL}/rest/api/2/filter/{filter_id}"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def search_with_filter(filter_id, max_results=50):
    """Search for issues using a saved filter"""
    # First get the filter details to get the JQL
    filter_details = get_filter_details(filter_id)
    if not filter_details:
        return None
    
    jql_query = filter_details.get("jql", "")
    if not jql_query:
        print(f"Filter {filter_id} does not contain a JQL query")
        return None
    
    # Now search using the JQL
    return search_issues(jql_query, max_results)

def search_issues(jql_query, max_results=50):
    """Search for issues using a JQL query"""
    url = f"{JIRA_BASE_URL}/rest/api/2/search"
    params = {
        "jql": jql_query,
        "maxResults": max_results
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def create_issue(project_key, summary, description, issue_type="Task", priority="Medium"):
    """Create a new issue in Jira"""
    url = f"{JIRA_BASE_URL}/rest/api/2/issue"
    
    # Prepare the issue data
    issue_data = {
        "fields": {
            "project": {
                "key": project_key
            },
            "summary": summary,
            "description": description,
            "issuetype": {
                "name": issue_type
            },
            "priority": {
                "name": priority
            }
        }
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(issue_data))
    
    if response.status_code in [200, 201]:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def update_issue(issue_key, fields_to_update):
    """Update an existing issue in Jira
    
    Args:
        issue_key (str): The key of the issue to update (e.g., 'NCIPT-12345')
        fields_to_update (dict): Dictionary of fields to update
            Example: {'summary': 'New summary', 'description': 'New description'}
    """
    url = f"{JIRA_BASE_URL}/rest/api/2/issue/{issue_key}"
    
    # Prepare the update data
    update_data = {
        "fields": fields_to_update
    }
    
    response = requests.put(url, headers=headers, data=json.dumps(update_data))
    
    if response.status_code in [200, 204]:
        print(f"Issue {issue_key} updated successfully")
        return True
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return False

def add_comment(issue_key, comment_text):
    """Add a comment to an existing issue
    
    Args:
        issue_key (str): The key of the issue to comment on
        comment_text (str): The text of the comment
    """
    url = f"{JIRA_BASE_URL}/rest/api/2/issue/{issue_key}/comment"
    
    comment_data = {
        "body": comment_text
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(comment_data))
    
    if response.status_code in [200, 201]:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def transition_issue(issue_key, transition_name):
    """Transition an issue to a different status
    
    Args:
        issue_key (str): The key of the issue to transition
        transition_name (str): The name of the transition (e.g., 'In Progress', 'Done')
    """
    # First, get available transitions
    transitions_url = f"{JIRA_BASE_URL}/rest/api/2/issue/{issue_key}/transitions"
    response = requests.get(transitions_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error getting transitions: {response.status_code}")
        print(response.text)
        return False
    
    transitions = response.json()["transitions"]
    transition_id = None
    
    # Find the transition ID for the requested transition name
    for transition in transitions:
        if transition["name"].lower() == transition_name.lower():
            transition_id = transition["id"]
            break
    
    if not transition_id:
        print(f"Transition '{transition_name}' not found. Available transitions:")
        for transition in transitions:
            print(f"- {transition['name']}")
        return False
    
    # Perform the transition
    transition_data = {
        "transition": {
            "id": transition_id
        }
    }
    
    response = requests.post(
        transitions_url, 
        headers=headers, 
        data=json.dumps(transition_data)
    )
    
    if response.status_code in [200, 204]:
        print(f"Issue {issue_key} transitioned to '{transition_name}' successfully")
        return True
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return False

def get_projects(max_results=50):
    """Get a list of all projects the user has access to"""
    url = f"{JIRA_BASE_URL}/rest/api/2/project"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def get_project_details(project_key):
    """Get detailed information about a specific project"""
    url = f"{JIRA_BASE_URL}/rest/api/2/project/{project_key}"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def get_boards(max_results=50):
    """Get a list of all boards the user has access to"""
    url = f"{JIRA_BASE_URL}/rest/agile/1.0/board"
    params = {
        "maxResults": max_results
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def get_board_details(board_id):
    """Get detailed information about a specific board"""
    url = f"{JIRA_BASE_URL}/rest/agile/1.0/board/{board_id}"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def get_sprints(board_id, state=None, max_results=50):
    """Get sprints for a board
    
    Args:
        board_id (int): The ID of the board
        state (str, optional): Filter by sprint state (active, future, closed)
        max_results (int, optional): Maximum number of results to return
    """
    url = f"{JIRA_BASE_URL}/rest/agile/1.0/board/{board_id}/sprint"
    params = {
        "maxResults": max_results
    }
    
    if state:
        params["state"] = state
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def get_sprint_issues(board_id, sprint_id, max_results=50):
    """Get issues in a sprint
    
    Args:
        board_id (int): The ID of the board
        sprint_id (int): The ID of the sprint
        max_results (int, optional): Maximum number of results to return
    """
    url = f"{JIRA_BASE_URL}/rest/agile/1.0/board/{board_id}/sprint/{sprint_id}/issue"
    params = {
        "maxResults": max_results
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def display_filters(filters_data):
    """Display saved filters in a readable format"""
    if not filters_data:
        print("No saved filters found or invalid data")
        return
    
    print(f"\nFound {len(filters_data)} saved filters:")
    print("-" * 80)
    
    for filter_item in filters_data:
        filter_id = filter_item["id"]
        name = filter_item["name"]
        jql = filter_item.get("jql", "N/A")
        
        print(f"ID: {filter_id}")
        print(f"Name: {name}")
        print(f"JQL: {jql}")
        print("-" * 80)

def display_boards(boards_data):
    """Display boards in a readable format"""
    if not boards_data or "values" not in boards_data:
        print("No boards found or invalid data")
        return
    
    print(f"\nFound {boards_data['total']} boards. Displaying {len(boards_data['values'])}:")
    print("-" * 80)
    
    for board in boards_data["values"]:
        board_id = board["id"]
        name = board["name"]
        board_type = board.get("type", "N/A")
        
        print(f"ID: {board_id}")
        print(f"Name: {name}")
        print(f"Type: {board_type}")
        print("-" * 80)

def display_sprints(sprints_data):
    """Display sprints in a readable format"""
    if not sprints_data or "values" not in sprints_data:
        print("No sprints found or invalid data")
        return
    
    print(f"\nFound {sprints_data['total']} sprints. Displaying {len(sprints_data['values'])}:")
    print("-" * 80)
    
    for sprint in sprints_data["values"]:
        sprint_id = sprint["id"]
        name = sprint["name"]
        state = sprint.get("state", "N/A")
        
        print(f"ID: {sprint_id}")
        print(f"Name: {name}")
        print(f"State: {state}")
        
        if "startDate" in sprint:
            print(f"Start Date: {sprint['startDate']}")
        if "endDate" in sprint:
            print(f"End Date: {sprint['endDate']}")
        
        print("-" * 80)

def display_projects(projects_data):
    """Display projects in a readable format"""
    if not projects_data:
        print("No projects found or invalid data")
        return
    
    print(f"\nFound {len(projects_data)} projects:")
    print("-" * 80)
    
    for project in projects_data:
        key = project["key"]
        name = project["name"]
        project_type = project.get("projectTypeKey", "N/A")
        
        print(f"Key: {key}")
        print(f"Name: {name}")
        print(f"Type: {project_type}")
        print("-" * 80)

def display_project_details(project_data):
    """Display detailed project information"""
    if not project_data:
        print("No project data found")
        return
    
    print("\nProject Details:")
    print("-" * 80)
    print(f"Key: {project_data['key']}")
    print(f"Name: {project_data['name']}")
    print(f"ID: {project_data['id']}")
    
    if "description" in project_data and project_data["description"]:
        print(f"Description: {project_data['description']}")
    
    if "lead" in project_data:
        print(f"Lead: {project_data['lead'].get('displayName', 'N/A')}")
    
    if "issueTypes" in project_data:
        print("\nIssue Types:")
        for issue_type in project_data["issueTypes"]:
            print(f"- {issue_type['name']}")
    
    print("-" * 80)

def display_issues(issues_data):
    """Display issues in a readable format"""
    if not issues_data or "issues" not in issues_data:
        print("No issues found or invalid data")
        return
    
    print(f"\nFound {issues_data['total']} issues. Displaying {len(issues_data['issues'])}:")
    print("-" * 80)
    
    for issue in issues_data["issues"]:
        key = issue["key"]
        summary = issue["fields"]["summary"]
        status = issue["fields"]["status"]["name"]
        issue_type = issue["fields"]["issuetype"]["name"]
        priority = issue["fields"].get("priority", {}).get("name", "No priority")
        
        print(f"Key: {key}")
        print(f"Type: {issue_type}")
        print(f"Summary: {summary}")
        print(f"Status: {status}")
        print(f"Priority: {priority}")
        print("-" * 80)

def display_created_issue(issue_data):
    """Display information about a newly created issue"""
    if not issue_data or "key" not in issue_data:
        print("Invalid issue data")
        return
    
    print("\nIssue created successfully:")
    print("-" * 80)
    print(f"Key: {issue_data['key']}")
    print(f"ID: {issue_data['id']}")
    print(f"Self: {issue_data['self']}")
    print("-" * 80)
    print(f"View issue: {JIRA_BASE_URL}/browse/{issue_data['key']}")

def search_issues_structured(jql_query, max_results=50, output_format="text"):
    """Search for issues and return in the specified format"""
    issues_data = search_issues(jql_query, max_results)
    
    if not issues_data or "issues" not in issues_data:
        return None
    
    if output_format == "json":
        return issues_data
    elif output_format == "simplified_json":
        # Create a simplified structure optimized for LLM processing
        simplified_issues = []
        for issue in issues_data["issues"]:
            try:
                simplified_issue = {
                    "key": issue["key"],
                    "summary": issue["fields"]["summary"] if issue["fields"] is not None and "summary" in issue["fields"] else "No summary",
                    "description": issue["fields"].get("description", "") if issue["fields"] is not None else "",
                    "status": issue["fields"]["status"]["name"] if issue["fields"] is not None and "status" in issue["fields"] and issue["fields"]["status"] is not None else "Unknown",
                    "issue_type": issue["fields"]["issuetype"]["name"] if issue["fields"] is not None and "issuetype" in issue["fields"] and issue["fields"]["issuetype"] is not None else "Unknown",
                    "priority": issue["fields"].get("priority", {}).get("name", "No priority") if issue["fields"] is not None else "No priority",
                    "created": issue["fields"]["created"] if issue["fields"] is not None and "created" in issue["fields"] else "",
                    "updated": issue["fields"]["updated"] if issue["fields"] is not None and "updated" in issue["fields"] else "",
                    "assignee": issue["fields"].get("assignee", {}).get("displayName", "Unassigned") if issue["fields"] is not None else "Unassigned",
                    "reporter": issue["fields"].get("reporter", {}).get("displayName", "Unknown") if issue["fields"] is not None else "Unknown",
                    "components": [c["name"] for c in issue["fields"].get("components", [])] if issue["fields"] is not None else [],
                    "labels": issue["fields"].get("labels", []) if issue["fields"] is not None else [],
                    "comments": []
                }
                
                # Add comments if available
                if issue["fields"] is not None and "comment" in issue["fields"] and issue["fields"]["comment"] is not None and "comments" in issue["fields"]["comment"]:
                    for comment in issue["fields"]["comment"]["comments"]:
                        simplified_issue["comments"].append({
                            "author": comment.get("author", {}).get("displayName", "Unknown"),
                            "body": comment.get("body", ""),
                            "created": comment.get("created", "")
                        })
                
                simplified_issues.append(simplified_issue)
            except Exception as e:
                # Print error to stderr instead of stdout
                print(f"Error processing issue {issue.get('key', 'unknown')}: {e}", file=sys.stderr)
                # Add a minimal issue entry with just the key
                simplified_issues.append({
                    "key": issue.get("key", "unknown"),
                    "summary": "Error processing issue",
                    "description": f"Error: {str(e)}",
                    "status": "Unknown",
                    "issue_type": "Unknown",
                    "priority": "Unknown",
                    "created": "",
                    "updated": "",
                    "assignee": "Unknown",
                    "reporter": "Unknown",
                    "components": [],
                    "labels": [],
                    "comments": []
                })
                continue
        return {"issues": simplified_issues, "total": issues_data["total"]}
    else:  # text format
        display_issues(issues_data)
        return None

def interactive_issue_selector(issues):
    """Present an interactive selector for issues"""
    try:
        import inquirer
    except ImportError:
        print("Please install the 'inquirer' package: pip install inquirer")
        return None
    
    if not issues or "issues" not in issues or not issues["issues"]:
        print("No issues to select from")
        return None
    
    choices = [
        f"{issue['key']} - {issue['issue_type']} - {issue['summary'][:50]}..." 
        for issue in issues["issues"]
    ]
    
    questions = [
        inquirer.List('issue',
                      message="Select an issue to analyze",
                      choices=choices,
                     )
    ]
    
    answers = inquirer.prompt(questions)
    if not answers:
        return None
    
    selected_key = answers['issue'].split(' - ')[0]
    for issue in issues["issues"]:
        if issue["key"] == selected_key:
            return issue
    
    return None

def analyze_issue_with_rag(issue, past_issues_db_path="past_issues.json"):
    """Analyze an issue using RAG to find similar past issues and suggest solutions"""
    try:
        import openai
        import json
        from sentence_transformers import SentenceTransformer
        import numpy as np
        from scipy.spatial.distance import cosine
    except ImportError:
        print("Please install required packages: pip install openai sentence-transformers numpy scipy")
        return None
    
    # Load past issues
    try:
        with open(past_issues_db_path, 'r') as f:
            past_issues = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        past_issues = {"issues": []}
    
    # Create embeddings for the current issue
    model = SentenceTransformer('all-MiniLM-L6-v2')
    current_text = f"{issue['summary']} {issue['description']}"
    current_embedding = model.encode(current_text)
    
    # Find similar issues
    similar_issues = []
    for past_issue in past_issues["issues"]:
        past_text = f"{past_issue['summary']} {past_issue['description']}"
        past_embedding = np.array(past_issue.get('embedding', model.encode(past_text)))
        
        # Calculate similarity
        similarity = 1 - cosine(current_embedding, past_embedding)
        if similarity > 0.7:  # Threshold for similarity
            similar_issues.append({
                "issue": past_issue,
                "similarity": similarity,
                "resolution": past_issue.get("resolution", "")
            })
    
    # Sort by similarity
    similar_issues.sort(key=lambda x: x["similarity"], reverse=True)
    
    # Use LLM to analyze and suggest solutions
    prompt = f"""
    I'm working on this Jira issue:
    
    Key: {issue['key']}
    Type: {issue['issue_type']}
    Summary: {issue['summary']}
    Description: {issue['description']}
    Status: {issue['status']}
    Priority: {issue['priority']}
    
    """
    
    if similar_issues:
        prompt += "Here are similar issues that were resolved in the past:\n\n"
        for i, similar in enumerate(similar_issues[:3]):  # Top 3 similar issues
            prompt += f"Similar Issue {i+1} (Similarity: {similar['similarity']:.2f}):\n"
            prompt += f"Key: {similar['issue']['key']}\n"
            prompt += f"Summary: {similar['issue']['summary']}\n"
            prompt += f"Resolution: {similar['resolution']}\n\n"
    
    prompt += "Based on this information, please analyze this issue and suggest how to approach it. If there are similar past issues, explain how their resolutions might apply to this case."
    
    # Call OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert software developer and project manager who helps analyze and solve Jira issues."},
            {"role": "user", "content": prompt}
        ]
    )
    
    analysis = response.choices[0].message.content
    
    return {
        "issue": issue,
        "similar_issues": similar_issues[:3] if similar_issues else [],
        "analysis": analysis
    }

def jira_rag_workflow(jql_query="assignee = currentUser() AND statusCategory != Done", max_results=20):
    """Complete workflow for Jira issue analysis with RAG"""
    # Fetch issues
    print(f"Fetching issues with query: {jql_query}")
    issues = search_issues_structured(jql_query, max_results, "simplified_json")
    
    if not issues or not issues.get("issues"):
        print("No issues found matching the query")
        return
    
    print(f"Found {issues['total']} issues. Displaying {len(issues['issues'])} for selection.")
    
    # Display a summary of issues
    for i, issue in enumerate(issues["issues"]):
        print(f"{i+1}. {issue['key']} - {issue['status']} - {issue['summary'][:50]}...")
    
    # Select an issue
    selected_issue = interactive_issue_selector(issues)
    if not selected_issue:
        print("No issue selected")
        return
    
    print(f"\nAnalyzing issue {selected_issue['key']}...")
    
    # Analyze with RAG
    analysis_result = analyze_issue_with_rag(selected_issue)
    
    if not analysis_result:
        print("Analysis failed")
        return
    
    # Display results
    print("\n" + "="*80)
    print(f"ANALYSIS FOR ISSUE {selected_issue['key']}")
    print("="*80)
    print(analysis_result["analysis"])
    print("\n" + "="*80)
    
    if analysis_result["similar_issues"]:
        print("\nSIMILAR PAST ISSUES:")
        for i, similar in enumerate(analysis_result["similar_issues"]):
            print(f"\n{i+1}. {similar['issue']['key']} (Similarity: {similar['similarity']:.2f})")
            print(f"   Summary: {similar['issue']['summary']}")
            print(f"   Resolution: {similar['resolution']}")
    
    # Ask if the user wants to save this resolution for future reference
    try:
        import inquirer
        questions = [
            inquirer.Confirm('save',
                            message="Would you like to save your resolution to this issue for future reference?",
                            default=False)
        ]
        answers = inquirer.prompt(questions)
        
        if answers and answers['save']:
            resolution = input("Please enter the resolution approach you used: ")
            
            # Save to past issues database
            try:
                with open("past_issues.json", 'r') as f:
                    past_issues = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                past_issues = {"issues": []}
            
            # Add embedding to the issue for future similarity comparison
            model = SentenceTransformer('all-MiniLM-L6-v2')
            issue_text = f"{selected_issue['summary']} {selected_issue['description']}"
            embedding = model.encode(issue_text).tolist()
            
            selected_issue["embedding"] = embedding
            selected_issue["resolution"] = resolution
            
            past_issues["issues"].append(selected_issue)
            
            with open("past_issues.json", 'w') as f:
                json.dump(past_issues, f, indent=2)
            
            print("Resolution saved for future reference")
    except ImportError:
        print("Install 'inquirer' for interactive prompts: pip install inquirer")

def show_future_features():
    """Display information about planned future features"""
    print("\n=== FUTURE ENHANCEMENTS ===\n")
    print("The following features are planned for future releases:")
    
    print("\n1. LLM and RAG Integration")
    print("   - Analyze issues using LLMs to suggest solutions")
    print("   - Find similar past issues using semantic search")
    print("   - Suggest resolutions based on how similar issues were resolved")
    
    print("\n2. Interactive Issue Selection")
    print("   - Text-based interactive interface for selecting issues")
    print("   - Side-by-side comparison of similar issues")
    
    print("\n3. Web Interface")
    print("   - Visual dashboard of your Jira issues")
    print("   - Point-and-click interface for issue analysis")
    
    print("\n4. Chat Platform Integration")
    print("   - Slack integration for Jira operations")
    print("   - Microsoft Teams integration")
    
    print("\nThese features are in development and will be released in future versions.")
    print("For more information, see the 'future' directory in the project repository.")

def main():
    parser = argparse.ArgumentParser(description="Jira API Interface")
    parser.add_argument("--action", 
                        choices=["user", "my-issues", "my-unresolved-issues", "search", "create", "update", 
                                "comment", "transition", "projects", "project-details",
                                "boards", "board-details", "sprints", "sprint-issues",
                                "filters", "filter-details", "search-with-filter", "future-features"], 
                        default="user", help="Action to perform (default: user)")
    parser.add_argument("--max-results", type=int, default=10, 
                        help="Maximum number of results to return (default: 10)")
    parser.add_argument("--jql", type=str, 
                        help="JQL query for searching issues (required for search action)")
    parser.add_argument("--project", type=str, 
                        help="Project key for creating issues or getting project details")
    parser.add_argument("--summary", type=str, 
                        help="Summary for the new issue (required for create action)")
    parser.add_argument("--description", type=str, 
                        help="Description for the new issue (required for create action)")
    parser.add_argument("--issue-type", type=str, default="Task", 
                        help="Issue type for the new issue (default: Task)")
    parser.add_argument("--priority", type=str, default="Medium", 
                        help="Priority for the new issue (default: Medium)")
    parser.add_argument("--issue-key", type=str,
                        help="Issue key for update/comment/transition actions (e.g., NCIPT-12345)")
    parser.add_argument("--comment", type=str,
                        help="Comment text to add to an issue (required for comment action)")
    parser.add_argument("--transition", type=str,
                        help="Transition name to apply to an issue (required for transition action)")
    parser.add_argument("--new-summary", type=str,
                        help="New summary for update action")
    parser.add_argument("--new-description", type=str,
                        help="New description for update action")
    parser.add_argument("--new-priority", type=str,
                        help="New priority for update action")
    parser.add_argument("--board-id", type=int,
                        help="Board ID for board-details, sprints, and sprint-issues actions")
    parser.add_argument("--sprint-id", type=int,
                        help="Sprint ID for sprint-issues action")
    parser.add_argument("--sprint-state", type=str, choices=["active", "future", "closed"],
                        help="Sprint state filter for sprints action")
    parser.add_argument("--filter-id", type=int,
                        help="Filter ID for filter-details and search-with-filter actions")
    parser.add_argument("--output-format", choices=["text", "json", "simplified_json"], 
                        default="text", help="Output format (default: text)")
    
    args = parser.parse_args()
    
    if args.action == "user":
        user_info = get_current_user()
        if user_info:
            print("Current User Information:")
            print(f"Name: {user_info.get('displayName', 'N/A')}")
            print(f"Email: {user_info.get('emailAddress', 'N/A')}")
            print(f"Account ID: {user_info.get('accountId', 'N/A')}")
            
            # Uncomment to see all available user information
            # print(json.dumps(user_info, indent=2))
    
    elif args.action == "my-issues":
        issues = get_my_issues(args.max_results)
        display_issues(issues)
    
    elif args.action == "my-unresolved-issues":
        issues = get_my_unresolved_issues(args.max_results)
        display_issues(issues)
    
    elif args.action == "search":
        if not args.jql:
            print("Error: --jql parameter is required for search action")
            parser.print_help()
            return
        
        if args.output_format in ["json", "simplified_json"]:
            issues = search_issues_structured(args.jql, args.max_results, args.output_format)
            if issues:
                print(json.dumps(issues, indent=2))
        else:
            issues = search_issues(args.jql, args.max_results)
            display_issues(issues)
    
    elif args.action == "create":
        # Check required parameters
        if not args.project or not args.summary or not args.description:
            print("Error: --project, --summary, and --description are required for create action")
            parser.print_help()
            return
        
        issue = create_issue(
            project_key=args.project,
            summary=args.summary,
            description=args.description,
            issue_type=args.issue_type,
            priority=args.priority
        )
        
        if issue:
            display_created_issue(issue)
    
    elif args.action == "update":
        # Check required parameters
        if not args.issue_key:
            print("Error: --issue-key is required for update action")
            parser.print_help()
            return
        
        # Check if at least one update field is provided
        if not args.new_summary and not args.new_description and not args.new_priority:
            print("Error: At least one of --new-summary, --new-description, or --new-priority is required")
            return
        
        # Prepare fields to update
        fields_to_update = {}
        if args.new_summary:
            fields_to_update["summary"] = args.new_summary
        if args.new_description:
            fields_to_update["description"] = args.new_description
        if args.new_priority:
            fields_to_update["priority"] = {"name": args.new_priority}
        
        update_issue(args.issue_key, fields_to_update)
    
    elif args.action == "comment":
        # Check required parameters
        if not args.issue_key or not args.comment:
            print("Error: --issue-key and --comment are required for comment action")
            parser.print_help()
            return
        
        comment = add_comment(args.issue_key, args.comment)
        if comment:
            print(f"Comment added to {args.issue_key} successfully")
    
    elif args.action == "transition":
        # Check required parameters
        if not args.issue_key or not args.transition:
            print("Error: --issue-key and --transition are required for transition action")
            parser.print_help()
            return
        
        transition_issue(args.issue_key, args.transition)
    
    elif args.action == "projects":
        projects = get_projects(args.max_results)
        display_projects(projects)
    
    elif args.action == "project-details":
        if not args.project:
            print("Error: --project parameter is required for project-details action")
            parser.print_help()
            return
        
        project = get_project_details(args.project)
        display_project_details(project)
    
    elif args.action == "boards":
        boards = get_boards(args.max_results)
        display_boards(boards)
    
    elif args.action == "board-details":
        if not args.board_id:
            print("Error: --board-id parameter is required for board-details action")
            parser.print_help()
            return
        
        board = get_board_details(args.board_id)
        print(json.dumps(board, indent=2))
    
    elif args.action == "sprints":
        if not args.board_id:
            print("Error: --board-id parameter is required for sprints action")
            parser.print_help()
            return
        
        sprints = get_sprints(args.board_id, args.sprint_state, args.max_results)
        display_sprints(sprints)
    
    elif args.action == "sprint-issues":
        if not args.board_id or not args.sprint_id:
            print("Error: --board-id and --sprint-id parameters are required for sprint-issues action")
            parser.print_help()
            return
        
        issues = get_sprint_issues(args.board_id, args.sprint_id, args.max_results)
        display_issues(issues)
    
    elif args.action == "filters":
        filters = get_saved_filters()
        display_filters(filters)
    
    elif args.action == "filter-details":
        if not args.filter_id:
            print("Error: --filter-id parameter is required for filter-details action")
            parser.print_help()
            return
        
        filter_details = get_filter_details(args.filter_id)
        print(json.dumps(filter_details, indent=2))
    
    elif args.action == "search-with-filter":
        if not args.filter_id:
            print("Error: --filter-id parameter is required for search-with-filter action")
            parser.print_help()
            return
        
        issues = search_with_filter(args.filter_id, args.max_results)
        display_issues(issues)

    elif args.action == "future-features":
        show_future_features()

if __name__ == "__main__":
    main()
