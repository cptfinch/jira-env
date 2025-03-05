{
  description = "Development shell with jira-cli and Python for Jira API interaction";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };
        
        # Create a Python environment with the required packages
        pythonEnv = pkgs.python3.withPackages (ps: with ps; [
          requests
          # Add other Python packages as needed
        ]);
      in
      {
        devShells.default = pkgs.mkShell {
          packages = [
            pkgs.jira-cli-go
            pythonEnv
            # Development tools
            pkgs.python3Packages.pip
            pkgs.python3Packages.black  # Python formatter
            pkgs.python3Packages.flake8 # Python linter
          ];
          
          # Shell hook to display Python version and available packages
          shellHook = ''
            echo "Python environment ready with the following:"
            echo "Python version: $(python --version)"
            echo "Requests package: $(python -c 'import requests; print(f"requests {requests.__version__}")')"
            echo ""
            echo "Use 'python jira-interface.py' to run your Jira interface script"
          '';
        };
      });
}

