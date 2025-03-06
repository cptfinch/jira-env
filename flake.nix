{
  description = "Jira Environment - A comprehensive interface to the Jira API";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    home-manager = {
      url = "github:nix-community/home-manager";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, home-manager }:
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
          
          # Development tools
          pytest
          black
          flake8
          mypy
        ]);
      in
      {
        # Expose the package
        packages = {
          default = jira-env;
          jira-env = jira-env;
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
          ];
          
          # Shell hook to display Python version and available packages
          shellHook = ''
            echo "Jira Environment development shell"
            echo "Python version: $(python --version)"
            echo "Requests package: $(python -c 'import requests; print(f"requests {requests.__version__}")')"
            echo "PyYAML package: $(python -c 'import yaml; print(f"pyyaml {yaml.__version__}")')"
            echo ""
            echo "Available commands:"
            echo "  jira-interface - Command-line interface"
            echo "  jira-export - Export Jira queries"
            echo "  jira-web - Start the web interface"
            echo ""
            echo "For development, you can run:"
            echo "  pip install -e ."
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
                type = lib.types.listOf (lib.types.enum ["rag", "web", "chat", "interactive", "all"]);
                default = [];
                description = "List of extensions to enable";
                example = ["web" "interactive"];
              };
            };
            
            config = lib.mkIf cfg.enable {
              home.packages = [ jira-env ];
              
              home.file.".config/jira-env/config.env" = lib.mkIf (!cfg.useApiTokenFromEnv && cfg.apiToken != "") {
                text = ''
                  JIRA_BASE_URL="${cfg.baseUrl}"
                  JIRA_API_TOKEN="${cfg.apiToken}"
                '';
              };
              
              home.sessionVariables = lib.mkIf (cfg.useApiTokenFromEnv || cfg.apiToken == "") {
                JIRA_BASE_URL = cfg.baseUrl;
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