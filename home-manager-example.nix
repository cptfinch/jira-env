# Example home-manager configuration for integrating jira-env
# Add this to your home.nix or similar file

{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    home-manager = {
      url = "github:nix-community/home-manager";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    jira-env = {
      url = "github:cptfinch/jira-env";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, home-manager, jira-env, ... }:
    let
      system = "x86_64-linux"; # Adjust for your system
      pkgs = nixpkgs.legacyPackages.${system};
    in {
      homeConfigurations."yourusername" = home-manager.lib.homeManagerConfiguration {
        inherit pkgs;
        
        modules = [
          jira-env.homeManagerModule
          
          {
            home.username = "yourusername";
            home.homeDirectory = "/home/yourusername";
            home.stateVersion = "23.11"; # Adjust for your version
            
            # Enable and configure jira-interface
            programs.jira-interface = {
              enable = true;
              baseUrl = "https://your-jira-instance.atlassian.net";
              useApiTokenFromEnv = true; # Recommended for security
            };
            
            # Other home-manager configurations...
          }
        ];
      };
    };
} 