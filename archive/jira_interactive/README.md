# Jira Interactive Selection

This package provides interactive interfaces for selecting and working with Jira issues.

## Planned Features

- Terminal UI for selecting issues
- Issue comparison for side-by-side analysis
- Batch operations on multiple selected issues

## Implementation Plan

The interactive selection tools will be implemented using terminal UI libraries and will provide:

1. **Issue Browser**: Navigate and select issues using arrow keys
2. **Comparison View**: Compare multiple issues side by side
3. **Batch Operations**: Perform actions on multiple issues at once
4. **Filtering and Sorting**: Interactive filtering and sorting of issues

## Getting Started (Future)

```python
# This is how the API will work when implemented
from jira_interactive import selector

# Select an issue interactively
selected_issue = selector.select_issue(jql="project = DEMO")

# Perform batch operations
selector.batch_update(jql="project = DEMO", field="priority", value="High")
```

## Dependencies (Planned)

- textual or rich (for terminal UI)
- prompt_toolkit (for interactive prompts)
- tabulate (for table formatting)
- jira-interface core package 