{
  description = "Jira API Interface - A command-line tool for interacting with Jira's REST API";

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
        
        # Define the package directly in the flake
        jira-interface = pkgs.python3Packages.buildPythonApplication {
          pname = "jira-interface";
          version = "0.1.0";
          
          src = ./.;
          
          propagatedBuildInputs = with pkgs.python3Packages; [
            requests
            pyyaml
          ];
          
          nativeBuildInputs = [ pkgs.makeWrapper ];
          
          # No build system, just install the script
          format = "other";
          
          installPhase = ''
            mkdir -p $out/bin $out/share/jira-interface
            cp jira-interface.py $out/bin/jira-interface
            cp jira_export_manager.py $out/bin/jira-export-manager
            cp config.env.example $out/share/jira-interface/
            cp setup_env.sh $out/share/jira-interface/
            cp jira_queries.yaml $out/share/jira-interface/
            chmod +x $out/bin/jira-interface $out/bin/jira-export-manager
            wrapProgram $out/bin/jira-interface \
              --set PYTHONPATH $PYTHONPATH
            wrapProgram $out/bin/jira-export-manager \
              --set PYTHONPATH $PYTHONPATH
          '';
          
          meta = with pkgs.lib; {
            description = "A command-line tool for interacting with Jira's REST API";
            homepage = "https://github.com/cptfinch/jira-env";
            license = licenses.mit;
            maintainers = with maintainers; [ /* add yourself here */ ];
            platforms = platforms.all;
          };
        };
        
        # Create a Python environment with the required packages
        pythonEnv = pkgs.python3.withPackages (ps: with ps; [
          requests
          pyyaml
          # Add other Python packages as needed
        ]);
      in
      {
        # Expose the package
        packages = {
          default = jira-interface;
          jira-interface = jira-interface;
        };

        # Development shell
        devShells.default = pkgs.mkShell {
          packages = [
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
            echo "PyYAML package: $(python -c 'import yaml; print(f"pyyaml {yaml.__version__}")')"
            echo ""
            echo "Use 'python jira-interface.py' to run your Jira interface script"
          '';
        };

        # Home Manager module
        homeManagerModules.default = { config, lib, pkgs, ... }: 
          let 
            cfg = config.programs.jira-interface;
          in {
            options.programs.jira-interface = {
              enable = lib.mkEnableOption "Jira API Interface";
              
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
              home.packages = [ jira-interface ];
              
              home.file.".config/jira-interface/config.env" = lib.mkIf (!cfg.useApiTokenFromEnv && cfg.apiToken != "") {
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
            jira-interface-module = self.homeManagerModules.${pkgs.system}.default;
          in
            jira-interface-module;
      };
}

