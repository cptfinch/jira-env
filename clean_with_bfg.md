# Cleaning Git History with BFG Repo-Cleaner

The BFG Repo-Cleaner is a faster, simpler alternative to `git filter-branch` for removing sensitive data from Git repositories.

## Prerequisites

1. Download the BFG Repo-Cleaner JAR file from: https://rtyley.github.io/bfg-repo-cleaner/
2. Make sure you have Java installed on your system

## Steps to Clean Repository

1. Create a backup of your repository:
   ```bash
   cp -r your-repo your-repo-backup
   ```

2. Create a text file with the sensitive data to replace:
   ```bash
   cat > sensitive-data.txt << EOF
   YOUR_API_TOKEN_HERE==>YOUR_API_TOKEN_HERE
   your-jira-instance.atlassian.net==>your-jira-instance.atlassian.net
   EOF
   ```

3. Run BFG to replace the sensitive data:
   ```bash
   java -jar bfg.jar --replace-text sensitive-data.txt your-repo.git
   ```

4. Change to your repository directory:
   ```bash
   cd your-repo
   ```

5. Clean up the repository:
   ```bash
   git reflog expire --expire=now --all
   git gc --prune=now --aggressive
   ```

6. Force push the changes to your remote repository:
   ```bash
   git push --force origin your-branch-name
   ```

## Important Notes

- This is a destructive operation that rewrites Git history
- All collaborators will need to clone the repository again after this operation
- Make sure you have a backup before proceeding
- After cleaning, verify that the sensitive data has been removed by checking the Git history

## Additional Resources

- BFG Repo-Cleaner documentation: https://rtyley.github.io/bfg-repo-cleaner/
- GitHub guide on removing sensitive data: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository 