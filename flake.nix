{
  description = "Jira Environment - A comprehensive interface to the Jira API";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    home-manager = {
      url = "github:nix-community/home-manager";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    jira-env.url = "github:cptfinch/jira-env";
  };

  outputs = { self, nixpkgs, flake-utils, home-manager, jira-env }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };
        
        # Define the Python package with all dependencies
        jira-env = pkgs.python3Packages.buildPythonPackage {
          pname = "jira-env";
          version = "0.1.0";
          
          src = ./.;
          
          propagatedBuildInputs = with pkgs.python3Packages; [
            # Core requirements
            requests
            pyyaml
            python-dotenv
            
            # RAG requirements
            openai
            numpy
            scikitlearn
            faiss
            langchain
            
            # Web requirements
            flask
            streamlit
            plotly
            pandas
            
            # Chat requirements
            slackclient
            botbuilder-core
            discordpy
            
            # Interactive requirements
            prompt-toolkit
            rich
            inquirer
          ];
          
          doCheck = false;  # Skip tests for now
          
          meta = with pkgs.lib; {
            description = "A comprehensive interface to the Jira API";
            homepage = "https://github.com/cptfinch/jira-env";
            license = licenses.mit;
            maintainers = with maintainers; [ /* add yourself here */ ];
            platforms = platforms.all;
          };
        };
        
        # Create a Python environment with the required packages
        pythonEnv = pkgs.python3.withPackages (ps: with ps; [
          # Core requirements
          requests
          pyyaml
          python-dotenv
          
          # Development tools
          pytest
          pytest-cov
          black
          flake8
          mypy
          
          # BDD testing
          behave
        ]);
        
        # Create a wrapper script for the CLI
        jira-cli-wrapper = pkgs.writeScriptBin "jira-cli" ''
          #!${pkgs.bash}/bin/bash
          export PYTHONPATH=${self}:$PYTHONPATH
          exec ${pythonEnv}/bin/python ${self}/jira-cli.py "$@"
        '';
      in
      {
        # Expose the package
        packages = {
          default = jira-env;
          jira-env = jira-env;
          jira-cli = jira-cli-wrapper;
        };

        # Add apps for nix run
        apps = {
          default = {
            type = "app";
            program = "${jira-cli-wrapper}/bin/jira-cli";
          };
          jira-cli = {
            type = "app";
            program = "${jira-cli-wrapper}/bin/jira-cli";
          };
        };

        # Development shell
        devShells.default = pkgs.mkShell {
          packages = [
            pythonEnv
            # Development tools
            pkgs.python3Packages.pip
            pkgs.python3Packages.black
            pkgs.python3Packages.flake8
            pkgs.python3Packages.mypy
            pkgs.python3Packages.pytest
            pkgs.python3Packages.pytest-cov
            pkgs.python3Packages.behave
          ];
          
          # Shell hook to display Python version and available packages
          shellHook = ''
            echo "Jira Environment development shell"
            echo "Python version: $(python --version)"
            echo "Requests package: $(python -c 'import requests; print(f"requests {requests.__version__}")')"
            echo "PyYAML package: $(python -c 'import yaml; print(f"pyyaml {yaml.__version__}")')"
            echo "python-dotenv package: $(python -c 'import dotenv; print(f"python-dotenv {dotenv.__version__ if hasattr(dotenv, "__version__") else "installed"}")')"
            echo ""
            echo "Available commands:"
            echo "  python cli.py --help - Run the command-line interface"
            echo "  python -m exports.manager - Run the export manager"
            echo ""
            echo "Note: The web interface module requires the package to be installed"
            echo "      as 'jira_env' to work properly. In development mode, you can"
            echo "      directly run: python web/interface.py"
            echo ""
            echo "For development:"
            echo "  All dependencies are already available in this nix shell environment."
            echo "  No need to run pip install - use 'nix develop' to manage dependencies."
            echo "  To add new dependencies, update the flake.nix file and run 'nix develop' again."
          '';
        };

        # Home Manager module
        homeManagerModules.default = { config, lib, pkgs, ... }: 
          let 
            cfg = config.programs.jira-env;
          in {
            options.programs.jira-env = {
              enable = lib.mkEnableOption "Jira Environment";
              
              baseUrl = lib.mkOption {
                type = lib.types.str;
                description = "Jira instance base URL";
                example = "https://your-jira-instance.atlassian.net";
              };
              
              useApiTokenFromEnv = lib.mkOption {
                type = lib.types.bool;
                default = true;
                description = "Whether to use the API token from the JIRA_API_TOKEN environment variable";
              };
              
              apiToken = lib.mkOption {
                type = lib.types.str;
                default = "";
                description = "Jira API token (not recommended, use environment variable instead)";
              };
              
              enableExtensions = lib.mkOption {
                type = lib.types.listOf (lib.types.enum ["rag" "web" "chat" "interactive" "all"]);
                default = [];
                description = "List of extensions to enable";
                example = ["web" "interactive"];
              };
            };
            
            config = lib.mkIf cfg.enable {
              home.packages = [ jira-env ];
              
              home.sessionVariables = {
                JIRA_BASE_URL = cfg.baseUrl;
              } // lib.optionalAttrs (!cfg.useApiTokenFromEnv && cfg.apiToken != "") {
                JIRA_API_TOKEN = cfg.apiToken;
              };
            };
          };
      }) // {
        # Make the Home Manager module available at the flake level
        homeManagerModule = { config, lib, pkgs, ... }:
          let
            jira-env-module = self.homeManagerModules.${pkgs.system}.default;
          in
            jira-env-module;
      };
} 