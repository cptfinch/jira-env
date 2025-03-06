#!/bin/bash

# Setup script for jira-interface

# Create config directory
mkdir -p ~/.config/jira-interface

# Check if config file already exists
if [ -f ~/.config/jira-interface/config.env ]; then
    echo "Config file already exists at ~/.config/jira-interface/config.env"
    echo "To recreate it, delete the existing file first."
else
    # Copy example config file
    if [ -f config.env.example ]; then
        cp config.env.example ~/.config/jira-interface/config.env
        echo "Created config file at ~/.config/jira-interface/config.env"
        echo "Please edit this file to add your Jira API token and base URL."
    else
        echo "Example config file not found. Creating a basic config file."
        cat > ~/.config/jira-interface/config.env << EOF
# Jira API Configuration

# Your Jira instance URL
JIRA_BASE_URL="https://your-jira-instance.atlassian.net"

# Your Jira API token
# Generate one at https://id.atlassian.com/manage-profile/security/api-tokens
JIRA_API_TOKEN="your-api-token-here"
EOF
        echo "Created config file at ~/.config/jira-interface/config.env"
        echo "Please edit this file to add your Jira API token and base URL."
    fi
fi

# Create jira_exports directory
mkdir -p jira_exports
echo "Created jira_exports directory for storing exported Jira data."

# Check if Python and required packages are installed
echo "Checking Python and required packages..."
python -c "import sys; print(f'Python version: {sys.version}')"

if python -c "import requests" 2>/dev/null; then
    echo "✅ requests package is installed"
else
    echo "❌ requests package is not installed"
    echo "Please install it with: pip install requests"
fi

if python -c "import yaml" 2>/dev/null; then
    echo "✅ pyyaml package is installed"
else
    echo "❌ pyyaml package is not installed"
    echo "Please install it with: pip install pyyaml"
fi

echo ""
echo "Setup complete! You can now use jira-interface.py"
echo "Example usage: python jira-interface.py --action my-issues"
echo ""
echo "Don't forget to edit ~/.config/jira-interface/config.env with your Jira credentials!" 