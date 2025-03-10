# Jira CLI

A simple command-line interface for searching Jira issues.

## Installation

### Using Nix

```bash
# Add to your home-manager configuration
{
  inputs.jira-env.url = "github:cptfinch/jira-env";
  
  outputs = { self, nixpkgs, home-manager, jira-env, ... }: {
    homeConfigurations."your-username" = home-manager.lib.homeManagerConfiguration {
      modules = [
        jira-env.homeManagerModule
        {
          programs.jira-env = {
            enable = true;
            baseUrl = "https://your-jira-instance.atlassian.net";
          };
        }
      ];
    };
  };
}
```

## Configuration

Set your Jira credentials using environment variables:

```bash
export JIRA_BASE_URL="https://your-jira-instance.atlassian.net"
export JIRA_API_TOKEN="your-api-token"
```

## Usage

The CLI supports searching Jira issues using either predefined queries or custom JQL:

```bash
# Search using a predefined query
jira-cli search --query all_my_issues
jira-cli search --query high_priority
jira-cli search --query recent_updates

# Search using custom JQL
jira-cli search --jql "project = PROJ AND created >= -30d"

# Control output format
jira-cli search --query all_my_issues --format json
jira-cli search --query all_my_issues --format table
jira-cli search --query all_my_issues --format summary

# Limit results
jira-cli search --query all_my_issues --limit 5

# List available predefined queries
jira-cli search --list-queries
```

## Predefined Queries

Queries are defined in `data/jira_queries.yaml`. Example queries:

```yaml
queries:
  - name: all_my_issues
    jql: "assignee = currentUser() AND statusCategory != Done"
    description: "All my unresolved issues across all projects"
  
  - name: high_priority
    jql: "assignee = currentUser() AND priority = High AND statusCategory != Done"
    description: "My high priority unresolved issues"
  
  - name: recent_updates
    jql: "assignee = currentUser() AND updated >= -7d"
    description: "My issues updated in the last week"
``` 