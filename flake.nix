{
  description = "Jira CLI - A simple interface for searching Jira issues";

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
        
        # Define the Python package with core dependencies
        jira-env = pkgs.python3Packages.buildPythonPackage {
          pname = "jira-env";
          version = "0.1.0";
          
          src = ./.;
          
          propagatedBuildInputs = with pkgs.python3Packages; [
            # Core requirements only
            requests
            pyyaml
            python-dotenv
          ];
          
          doCheck = false;  # Skip tests for now
          
          meta = with pkgs.lib; {
            description = "A simple interface for searching Jira issues";
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
          black
          flake8
          mypy
        ]);
        
        # Create a wrapper script for the CLI
        jira-cli-wrapper = pkgs.stdenv.mkDerivation {
          name = "jira-cli";
          
          buildInputs = [];
          src = ./.;
          
          dontConfigure = true;
          dontBuild = true;
          
          installPhase = ''
            # Create bin directory
            mkdir -p $out/bin
            
            # Create config directory
            mkdir -p $out/etc/jira-cli
            
            # Copy the queries file
            cp $src/data/jira_queries.yaml $out/etc/jira-cli/
            
            # Create the wrapper script
            cat > $out/bin/jira-cli << EOF
            #!${pkgs.bash}/bin/bash
            export PYTHONPATH=${self}:\$PYTHONPATH
            export JIRA_QUERIES_PATH=$out/etc/jira-cli/jira_queries.yaml
            exec ${pythonEnv}/bin/python ${self}/jira-cli.py "\$@"
            EOF
            
            chmod +x $out/bin/jira-cli
          '';
        };
      in
      {
        packages = {
          default = jira-env;
          jira-env = jira-env;
          jira-cli = jira-cli-wrapper;
        };

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

        devShells.default = pkgs.mkShell {
          packages = [
            pythonEnv
            pkgs.python3Packages.pip
            pkgs.python3Packages.black
            pkgs.python3Packages.flake8
            pkgs.python3Packages.mypy
            pkgs.python3Packages.pytest
          ];
          
          shellHook = ''
            echo "Jira CLI development shell"
            echo "Python version: $(python --version)"
            echo "Requests package: $(python -c 'import requests; print(f"requests {requests.__version__}")')"
            echo "PyYAML package: $(python -c 'import yaml; print(f"pyyaml {yaml.__version__}")')"
            echo "python-dotenv package: $(python -c 'import dotenv; print(f"python-dotenv {dotenv.__version__ if hasattr(dotenv, "__version__") else "installed"}")')"
            echo ""
            echo "Available commands:"
            echo "  jira-cli search --help - Show search command help"
            echo "  jira-cli search --list-queries - List available queries"
            echo ""
            echo "For development:"
            echo "  All dependencies are already available in this nix shell environment."
            echo "  To add new dependencies, update the flake.nix file and run 'nix develop' again."
          '';
        };

        # Home Manager module
        homeManagerModules.default = { config, lib, pkgs, ... }: 
          let 
            cfg = config.programs.jira-env;
          in {
            options.programs.jira-env = {
              enable = lib.mkEnableOption "Jira CLI";
              
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