#!/bin/bash

# Script to clean sensitive information from git history
# This is a destructive operation and will rewrite git history!

echo "WARNING: This script will rewrite git history to remove sensitive information."
echo "This is a destructive operation and cannot be undone."
echo "Make sure you have a backup of your repository before proceeding."
echo ""
echo "Press Enter to continue or Ctrl+C to abort..."
read

# Define patterns to remove
echo "Removing sensitive information from git history..."

# Use git filter-branch to remove sensitive information
git filter-branch --force --index-filter \
    "git ls-files -z | xargs -0 sed -i 's/NDE5Njk2NzkwMzA3OqkDNiz4\/pkddFSMljvMFYMOEtmy/YOUR_API_TOKEN_HERE/g; s/jira\.goiba\.net/your-jira-instance.atlassian.net/g'" \
    --prune-empty --tag-name-filter cat -- --all

# Force garbage collection to remove the old commits
echo "Cleaning up..."
git for-each-ref --format="delete %(refname)" refs/original | git update-ref --stdin
git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo ""
echo "Git history has been cleaned."
echo "To push these changes to your remote repository, you'll need to force push:"
echo "  git push --force origin your-branch-name"
echo ""
echo "IMPORTANT: All collaborators will need to clone the repository again after this operation." 