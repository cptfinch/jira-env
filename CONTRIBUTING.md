# Contributing to Jira API Interface

Thank you for considering contributing to the Jira API Interface! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project.

## How to Contribute

1. **Fork the repository** on GitHub
2. **Clone your fork** to your local machine
3. **Create a branch** for your changes
4. **Make your changes** and commit them with clear, descriptive messages
5. **Push your changes** to your fork
6. **Submit a pull request** to the main repository

## Development Setup

### Using Nix

If you have Nix installed, you can use the provided flake to set up a development environment:

```bash
nix develop
```

This will create an environment with Python and all required dependencies.

### Standard Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/cptfinch/jira-env.git
   cd jira-env
   ```

2. Install the required dependencies:
   ```bash
   pip install requests
   ```

## Coding Standards

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for Python code
- Write clear, descriptive commit messages
- Add docstrings to new functions and classes
- Update documentation when necessary

## Testing

Before submitting a pull request, please test your changes thoroughly:

1. Test with different Jira instances if possible
2. Test all affected functionality
3. Ensure your code doesn't break existing functionality

## Adding New Features

When adding new features:

1. First check if the feature is already planned or has been discussed in issues
2. Consider the scope of the feature and how it fits with the project's goals
3. Add appropriate documentation for the feature
4. Add examples of how to use the feature

## Reporting Bugs

When reporting bugs:

1. Check if the bug has already been reported
2. Include detailed steps to reproduce the bug
3. Include information about your environment (OS, Python version, etc.)
4. If possible, suggest a fix

## Pull Request Process

1. Update the README.md with details of changes if applicable
2. Update the documentation if necessary
3. The pull request will be reviewed by maintainers
4. Once approved, the pull request will be merged

Thank you for your contributions! 