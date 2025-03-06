"""
Jira Chat Integration Module

This package provides integration with chat platforms for the Jira API Interface,
enabling users to interact with Jira through chat interfaces like Slack, Discord, etc.
"""

__version__ = "0.1.0-alpha"

from jira_env.chat.integration import (
    JiraChatIntegration,
    SlackBot,
    TeamsBot,
    DiscordBot,
    start_slack_bot,
    start_teams_bot,
    start_discord_bot
)

__all__ = [
    'JiraChatIntegration',
    'SlackBot',
    'TeamsBot',
    'DiscordBot',
    'start_slack_bot',
    'start_teams_bot',
    'start_discord_bot'
] 