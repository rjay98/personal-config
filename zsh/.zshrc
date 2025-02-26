# Auto-completion
autoload -Uz compinit; compinit

# nvm config
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm


. "$HOME/.local/bin/env"

# pnpm
export PNPM_HOME="/Users/ryanjiang/Library/pnpm"
case ":$PATH:" in
  *":$PNPM_HOME:"*) ;;
  *) export PATH="$PNPM_HOME:$PATH" ;;
esac
# pnpm end

# alias
alias pikadeploy="git checkout prod && git pull --rebase origin main && git push --force"

# 1Password plugins
source /Users/ryanjiang/.config/op/plugins.sh

# zsh-autosuggestions
source $(brew --prefix)/share/zsh-autosuggestions/zsh-autosuggestions.zsh

# starship
eval "$(starship init zsh)"

. "/Users/ryanjiang/.deno/env"

# Keybinding fixes for terminals
bindkey "\e[1;3D" backward-word     # ⌥←
bindkey "\e[1;3C" forward-word      # ⌥→
bindkey "^[[1;9D" beginning-of-line # cmd+←
bindkey "^[[1;9C" end-of-line       # cmd+→

# Tailscale alias
alias tailscale="/Applications/Tailscale.app/Contents/MacOS/Tailscale"

# WORK-SPECIFIC CONFIG START
# Put any work-specific configurations here, and they won't be overridden
# Example: WORK_API_KEY="your-api-key"
# WORK-SPECIFIC CONFIG END
