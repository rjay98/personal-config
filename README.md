# Dotfiles

A curated collection of configuration files (dotfiles) for Vim, Zsh, and VSCode to enhance your development environment.

## Overview

This repository contains my personal dotfiles and configuration settings for various development tools. It includes a synchronization script that makes it easy to keep your configuration files up to date across multiple machines.

## What's Included

- **Vim**: Custom .vimrc configuration, color schemes, and plugin management
- **Zsh**: Shell configuration, aliases, and functions
- **VSCode**: Settings, keybindings, and recommended extensions

## Key Features

- 🔄 Synchronization script for easy setup on new machines
- 🔌 Vim plugin management with vim-plug and native packages
- 🎨 Gruvbox color scheme for Vim
- 🌲 NERDTree file explorer configuration
- 🔍 Intelligent work configuration preservation in Zsh
- 📋 Recommended VS Code extensions

## Installation

### Quick Start

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/dotfiles.git
   cd dotfiles
   ```

2. Run the sync script:
   ```bash
   uv run sync-settings.py
   ```

The script will:
- Create necessary directories
- Install vim-plug if not present
- Backup your existing configuration files
- Sync all dotfiles to their appropriate locations
- Preserve work-specific configurations in your .zshrc

### Manual Installation

If you prefer to install specific components manually:

#### Vim Setup
```bash
# Create necessary directories
mkdir -p ~/.vim/colors ~/.vim/autoload ~/.vim/pack/plugins/start

# Copy .vimrc
cp vim/.vimrc ~/.vimrc

# Install vim-plug
curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim

# Install plugins
vim -c 'PlugInstall' -c 'qa!'
```

#### Zsh Setup
```bash
# Copy Zsh configurations
cp zsh/.zshrc ~/.zshrc
cp zsh/.zsh_aliases ~/.zsh_aliases
cp zsh/.zsh_functions ~/.zsh_functions
```

#### VSCode Setup
```bash
# Copy VSCode configurations
cp -r vscode/settings.json "$HOME/Library/Application Support/Code/User/"
cp -r vscode/keybindings.json "$HOME/Library/Application Support/Code/User/"
cp -r vscode/snippets "$HOME/Library/Application Support/Code/User/"
```

## Vim Configuration Highlights

- **Plugin Management**: Supports both vim-plug and native Vim 8+ package management
- **Color Scheme**: Gruvbox theme with medium contrast
- **File Navigation**: NERDTree with custom key mappings
- **Key Mappings**:
  - `<Space>` as leader key
  - `<Leader>w` to save
  - `<Leader>q` to quit
  - `<Ctrl-n>` to toggle NERDTree
  - `<Leader>/` to clear search highlighting

## Customization

### Work-Specific Configurations

Your work-specific Zsh configuration is preserved between the markers:
```bash
# WORK-SPECIFIC CONFIG START
# Your work configuration here
# WORK-SPECIFIC CONFIG END
```

### Adding Vim Plugins

Edit `vim/plugins.vim` to add new plugins:
```vim
" Inside vim/plugins.vim
call plug#begin('~/.vim/plugged')
" Existing plugins...
Plug 'username/new-plugin'
call plug#end()
```

Then run `:PlugInstall` in Vim to install them.

## Maintenance

To update your dotfiles:

1. Make changes to the files in this repository
2. Run the sync script to update your local configuration
3. Commit and push your changes to keep the repository updated

## Contributing

Suggestions and improvements are welcome! Feel free to fork this repository and submit a pull request.

## License

MIT

---

*"Customize your tools until they feel like extensions of your hands."*
