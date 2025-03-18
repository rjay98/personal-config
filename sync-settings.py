#!/usr/bin/env python3
"""
Sync Settings Script

This script synchronizes configuration files for vim, zsh, and vscode
from a GitHub repository to their appropriate locations on a Mac.
It preserves work-specific configurations in .zshrc and installs
Homebrew packages from a list.
"""

import datetime
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

# Configuration
REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
HOME_DIR = str(Path.home())

# Define paths
CONFIG_PATHS = {
    'vim': {
        'source': os.path.join(REPO_ROOT, 'vim'),
        'files': {
            '.vimrc': os.path.join(HOME_DIR, '.vimrc'),
            'colors': os.path.join(HOME_DIR, '.vim', 'colors'),
            'autoload': os.path.join(HOME_DIR, '.vim', 'autoload'),
            'plugins.vim': os.path.join(HOME_DIR, '.vim', 'plugins.vim')
        }
    },
    'zsh': {
        'source': os.path.join(REPO_ROOT, 'zsh'),
        'files': {
            '.zshrc': os.path.join(HOME_DIR, '.zshrc'),
            '.zsh_aliases': os.path.join(HOME_DIR, '.zsh_aliases'),
            '.zsh_functions': os.path.join(HOME_DIR, '.zsh_functions'),
        }
    },
    'vscode': {
        'source': os.path.join(REPO_ROOT, 'vscode'),
        'files': {
            'settings.json': os.path.join(HOME_DIR, 'Library', 'Application Support', 'Code', 'User', 'settings.json'),
            'keybindings.json': os.path.join(HOME_DIR, 'Library', 'Application Support', 'Code', 'User', 'keybindings.json'),
            'snippets': os.path.join(HOME_DIR, 'Library', 'Application Support', 'Code', 'User', 'snippets'),
        }
    }
}

# Work-specific zshrc section markers
WORK_CONFIG_START = "# WORK-SPECIFIC CONFIG START"
WORK_CONFIG_END = "# WORK-SPECIFIC CONFIG END"


def print_header(message):
    """Print a formatted header message."""
    print("\n" + "=" * 60)
    print(f" {message}")
    print("=" * 60)


def backup_file(file_path):
    """Create a backup of a file with timestamp."""
    if os.path.exists(file_path):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{file_path}.bak_{timestamp}"
        try:
            shutil.copy2(file_path, backup_path)
            print(f"✅ Created backup: {backup_path}")
            return backup_path
        except Exception as e:
            print(f"❌ Failed to backup {file_path}: {e}")
    return None


def extract_work_config(zshrc_path):
    """Extract work-specific configuration from .zshrc file."""
    if not os.path.exists(zshrc_path):
        return ""
    
    with open(zshrc_path, 'r') as f:
        content = f.read()
    
    work_config_pattern = re.compile(
        f"{WORK_CONFIG_START}(.*?){WORK_CONFIG_END}", 
        re.DOTALL
    )
    
    match = work_config_pattern.search(content)
    if match:
        return f"{WORK_CONFIG_START}{match.group(1)}{WORK_CONFIG_END}"
    return ""


def merge_zshrc(repo_zshrc, home_zshrc, work_config):
    """Merge repository .zshrc with work-specific configuration."""
    with open(repo_zshrc, 'r') as f:
        content = f.read()
    
    # If work config exists and isn't already in the repo version
    if work_config and work_config not in content:
        # Replace existing work config section if it exists
        work_config_pattern = re.compile(
            f"{WORK_CONFIG_START}(.*?){WORK_CONFIG_END}", 
            re.DOTALL
        )
        
        if work_config_pattern.search(content):
            content = work_config_pattern.sub(work_config, content)
        else:
            # Append to the end if no section exists
            content += f"\n\n{work_config}\n"
    
    with open(home_zshrc, 'w') as f:
        f.write(content)
    
    print(f"✅ Merged work-specific configuration into {home_zshrc}")


def sync_vim_settings():
    """Sync Vim settings."""
    print_header("Syncing Vim Settings")
    
    vim_config = CONFIG_PATHS['vim']
    
    # Create .vim directory if it doesn't exist
    os.makedirs(os.path.join(HOME_DIR, '.vim'), exist_ok=True)
    os.makedirs(os.path.join(HOME_DIR, '.vim', 'colors'), exist_ok=True)
    os.makedirs(os.path.join(HOME_DIR, '.vim', 'autoload'), exist_ok=True)
    
    # Create directories for Vim's native package management
    plugin_path = os.path.join(HOME_DIR, '.vim', 'pack', 'plugins', 'start')
    os.makedirs(plugin_path, exist_ok=True)
    print(f"✅ Created Vim native package directory at {plugin_path}")
    
    # Sync .vimrc
    repo_vimrc = os.path.join(vim_config['source'], '.vimrc')
    home_vimrc = vim_config['files']['.vimrc']
    
    if os.path.exists(repo_vimrc):
        backup_file(home_vimrc)
        shutil.copy2(repo_vimrc, home_vimrc)
        print(f"✅ Synced .vimrc to {home_vimrc}")
    else:
        print(f"❌ Source .vimrc not found at {repo_vimrc}")
    
    # Sync color schemes
    repo_colors = os.path.join(vim_config['source'], 'colors')
    home_colors = vim_config['files']['colors']
    
    if os.path.exists(repo_colors) and os.path.isdir(repo_colors):
        for color_file in os.listdir(repo_colors):
            if color_file.endswith('.vim'):
                src = os.path.join(repo_colors, color_file)
                dst = os.path.join(home_colors, color_file)
                shutil.copy2(src, dst)
                print(f"✅ Synced color scheme: {color_file}")
    
    # Check for vim-plug and install if missing
    plug_path = os.path.join(HOME_DIR, '.vim', 'autoload', 'plug.vim')
    if not os.path.exists(plug_path):
        print("⏳ vim-plug not found. Installing...")
        try:
            curl_cmd = [
                'curl', '-fLo', plug_path, '--create-dirs',
                'https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
            ]
            subprocess.run(curl_cmd, check=True)
            print("✅ vim-plug installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install vim-plug: {e}")

    repo_plugins = os.path.join(vim_config['source'], 'plugins.vim')
    home_plugins = vim_config['files']['plugins.vim']

    if os.path.exists(repo_plugins):
        backup_file(home_plugins)
        shutil.copy2(repo_plugins, home_plugins)
        print(f"✅ Synced plugins.vim to {home_plugins}")
    else:
        print(f"❌ Source plugins.vim not found at {repo_plugins}")
            
    # Inform user about package management options
    print("\n💡 Tip: You now have two ways to manage Vim plugins:")
    print("  1. vim-plug: Add plugins to .vimrc and run :PlugInstall in Vim")
    print("  2. Native packages: Clone plugin repos directly to:")
    print(f"     {plugin_path}")


def sync_zsh_settings():
    """Sync Zsh settings while preserving work configurations."""
    print_header("Syncing Zsh Settings")
    
    zsh_config = CONFIG_PATHS['zsh']
    
    # Handle .zshrc special case with work configs
    repo_zshrc = os.path.join(zsh_config['source'], '.zshrc')
    home_zshrc = zsh_config['files']['.zshrc']
    
    if os.path.exists(repo_zshrc):
        # Extract work-specific config from existing .zshrc
        work_config = extract_work_config(home_zshrc)
        
        # Backup existing .zshrc
        backup_file(home_zshrc)
        
        # Merge configs
        merge_zshrc(repo_zshrc, home_zshrc, work_config)
    else:
        print(f"❌ Source .zshrc not found at {repo_zshrc}")
    
    # Sync other zsh files
    for filename, dest_path in zsh_config['files'].items():
        if filename != '.zshrc':  # Skip .zshrc as it's handled specially
            src_path = os.path.join(zsh_config['source'], filename)
            if os.path.exists(src_path):
                backup_file(dest_path)
                shutil.copy2(src_path, dest_path)
                print(f"✅ Synced {filename} to {dest_path}")
            else:
                print(f"❌ Source {filename} not found at {src_path}")


def sync_vscode_settings():
    """Sync VSCode settings."""
    print_header("Syncing VSCode Settings")
    
    vscode_config = CONFIG_PATHS['vscode']
    
    # Ensure VSCode settings directory exists
    vscode_dir = os.path.dirname(vscode_config['files']['settings.json'])
    os.makedirs(vscode_dir, exist_ok=True)
    os.makedirs(os.path.join(vscode_dir, 'snippets'), exist_ok=True)
    
    # Sync settings.json and keybindings.json
    for filename in ['settings.json', 'keybindings.json']:
        src_path = os.path.join(vscode_config['source'], filename)
        dest_path = vscode_config['files'][filename]
        
        if os.path.exists(src_path):
            backup_file(dest_path)
            shutil.copy2(src_path, dest_path)
            print(f"✅ Synced {filename} to {dest_path}")
        else:
            print(f"❌ Source {filename} not found at {src_path}")
    
    # Sync snippets
    src_snippets = os.path.join(vscode_config['source'], 'snippets')
    dest_snippets = vscode_config['files']['snippets']
    
    if os.path.exists(src_snippets) and os.path.isdir(src_snippets):
        for snippet_file in os.listdir(src_snippets):
            if snippet_file.endswith('.json'):
                src = os.path.join(src_snippets, snippet_file)
                dst = os.path.join(dest_snippets, snippet_file)
                backup_file(dst)
                shutil.copy2(src, dst)
                print(f"✅ Synced snippet: {snippet_file}")
    else:
        print(f"❌ Source snippets directory not found at {src_snippets}")
    
    # List of recommended VSCode extensions
    print("\n📋 Recommended VSCode extensions to install:")
    extensions_file = os.path.join(vscode_config['source'], 'extensions.txt')
    if os.path.exists(extensions_file):
        with open(extensions_file, 'r') as f:
            extensions = f.read().splitlines()
        
        for ext in extensions:
            if ext and not ext.startswith('#'):
                print(f"  - {ext}")
        
        print("\n💡 Install all extensions with:")
        print("  cat vscode/extensions.txt | grep -v '^#' | xargs -L 1 code --install-extension")
    else:
        print("❌ extensions.txt not found")


def install_homebrew_packages():
    """Install Homebrew packages from the homebrews.txt file."""
    print_header("Installing Homebrew Packages")
    
    brew_packages_file = os.path.join(REPO_ROOT, 'brew', 'homebrews.txt')
    
    if not os.path.exists(brew_packages_file):
        print(f"❌ Homebrew packages file not found at {brew_packages_file}")
        return
    
    # Check if Homebrew is installed
    try:
        subprocess.run(['which', 'brew'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print("❌ Homebrew is not installed. Please install Homebrew first.")
        print("💡 Install Homebrew with: /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
        return
    
    # Read packages from file
    with open(brew_packages_file, 'r') as f:
        packages = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    if not packages:
        print("ℹ️ No packages found in homebrews.txt")
        return
    
    print(f"📋 Found {len(packages)} packages to install")
    
    # Install each package
    for package in packages:
        print(f"⏳ Installing {package}...")
        try:
            # Using brew install with --force-bottle to prefer pre-built binaries
            result = subprocess.run(
                ['brew', 'install', package],
                check=False,  # Don't fail if already installed
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            if result.returncode == 0:
                print(f"✅ Installed {package}")
            else:
                # Check if it's already installed
                check_result = subprocess.run(
                    ['brew', 'list', package],
                    check=False,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                
                if check_result.returncode == 0:
                    print(f"ℹ️ Package {package} is already installed")
                else:
                    print(f"❌ Failed to install {package}: {result.stderr.strip()}")
        
        except Exception as e:
            print(f"❌ Error installing {package}: {e}")
    
    print("✅ Homebrew package installation complete")


def main():
    """Main function that runs the sync process."""
    print_header("Starting Settings Sync")
    print(f"Repository: {REPO_ROOT}")
    print(f"Home Directory: {HOME_DIR}")
    
    try:
        # Sync settings for each tool
        sync_vim_settings()
        sync_zsh_settings()
        sync_vscode_settings()
        
        # Install Homebrew packages
        install_homebrew_packages()
        
        print_header("Settings Sync Complete!")
        print("All your configuration files have been synced successfully!")
        print("Backups of your previous configurations were created.")
        print("\n💡 Tip: Restart your terminal for zsh changes to take effect.")
        print("💡 Tip: Run ':PlugInstall' in vim to install plugins.")
        
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
