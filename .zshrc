# Lines configured by zsh-newuser-install
HISTFILE=~/.histfile
HISTSIZE=1000
SAVEHIST=1000
bindkey -e
# End of lines configured by zsh-newuser-install
# The following lines were added by compinstall
zstyle :compinstall filename '/home/valblaze/.zshrc'

autoload -Uz compinit
compinit
# End of lines added by compinstall

# Source
plug "$HOME/.config/zsh/aliases.zsh"
plug "$HOME/.config/zsh/exports.zsh"
