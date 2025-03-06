#!/bin/bash

# Script to clean up sensitive data before making the repository public

echo "Cleaning up sensitive data before making the repository public..."

# Remove jira_exports directory contents but keep the directory
if [ -d "jira_exports" ]; then
    echo "Removing contents of jira_exports directory..."
    find jira_exports -type f -delete
    find jira_exports -type d -not -path "jira_exports" -delete
    touch jira_exports/.gitkeep
    echo "✅ jira_exports directory cleaned"
else
    echo "❌ jira_exports directory not found"
fi

# Remove any config files
if [ -f "config.env" ]; then
    echo "Removing config.env file..."
    rm config.env
    echo "✅ config.env removed"
fi

# Check for any remaining sensitive data
echo "Checking for any remaining sensitive data..."
SENSITIVE_FILES=$(grep -r "API_TOKEN.*=.*[a-zA-Z0-9]" --include="*.py" --include="*.json" --include="*.yaml" --include="*.yml" . | grep -v "example\|template\|config.env.example\|setup_env.sh\|cleanup_for_public.sh\|os.environ.get\|environment variable")

if [ -n "$SENSITIVE_FILES" ]; then
    echo "⚠️ Potential API tokens found in the following files:"
    echo "$SENSITIVE_FILES"
    echo "Please review these files manually before making the repository public."
else
    echo "✅ No API tokens found"
fi

# Check for any passwords
echo "Checking for passwords..."
PASSWORD_FILES=$(grep -r "password.*=.*[a-zA-Z0-9]" --include="*.py" --include="*.json" --include="*.yaml" --include="*.yml" . | grep -v "example\|template\|config.env.example\|setup_env.sh\|cleanup_for_public.sh\|os.environ.get\|environment variable")

if [ -n "$PASSWORD_FILES" ]; then
    echo "⚠️ Potential passwords found in the following files:"
    echo "$PASSWORD_FILES"
    echo "Please review these files manually before making the repository public."
else
    echo "✅ No passwords found"
fi

# Check for any URLs that might be specific to your organization
echo "Checking for organization-specific URLs..."
ORG_URLS=$(grep -r "jira\..*\.com\|jira\..*\.net\|atlassian\..*\.com\|atlassian\..*\.net" --include="*.py" --include="*.json" --include="*.yaml" --include="*.yml" --include="*.md" . | grep -v "example\|template\|your-jira-instance\|config.env.example\|id.atlassian.com")

if [ -n "$ORG_URLS" ]; then
    echo "⚠️ Organization-specific URLs found in the following files:"
    echo "$ORG_URLS"
    echo "Please review these files manually before making the repository public."
else
    echo "✅ No obvious organization-specific URLs found"
fi

# Check for sensitive data in git history
echo "Checking for sensitive data in git history..."
GIT_SENSITIVE=$(git log -p | grep -A 3 -B 3 "API_TOKEN.*=.*[a-zA-Z0-9]\|password.*=.*[a-zA-Z0-9]\|jira\.goiba\.net" | grep -v "example\|template\|your-jira-instance\|config.env.example\|os.environ.get\|environment variable")

if [ -n "$GIT_SENSITIVE" ]; then
    echo "⚠️ CRITICAL: Sensitive data found in git history!"
    echo "This is a serious security risk. You must clean the git history before making this repository public."
    echo "Use the provided clean_git_history.sh script or BFG Repo-Cleaner to remove sensitive data from the git history."
    echo "See clean_with_bfg.md for detailed instructions."
else
    echo "✅ No obvious sensitive data found in git history"
fi

echo ""
echo "Cleanup complete! Please review any warnings above before making the repository public."
echo "Remember to run 'git add .gitignore config.env.example setup_env.sh cleanup_for_public.sh clean_git_history.sh clean_with_bfg.md' to include these files in your repository." 