# Sample .bashrc for SUSE Linux
# Copyright (c) SUSE Software Solutions Germany GmbH

# There are 3 different types of shells in bash: the login shell, normal shell
# and interactive shell. Login shells read ~/.profile and interactive shells
# read ~/.bashrc; in our setup, /etc/profile sources ~/.bashrc - thus all
# settings made here will also take effect in a login shell.
#
# NOTE: It is recommended to make language settings in ~/.profile rather than
# here, since multilingual X sessions would not work properly if LANG is over-
# ridden in every subshell.

# ______________
# custom alias

# general
alias config='/usr/bin/git --git-dir="$HOME/.dotfiles/" --work-tree="$HOME"'

# vim
alias svim="sudo vim"

# navigation
alias ls="ls --color=auto"
alias ls.="ls -d .* --color=auto"
alias cd.="cd ~"

# zypper/flatpak/yast
alias zypper="sudo zypper"
alias appinfo="\zypper info"
alias appin="appinfo"
alias appsearch="\zypper search"
alias appse="appsearch"
alias update=".local/bin/update.sh"

alias flatpak="flatpak --user"

alias yast="su -c 'yast --qt'"

# additional
alias pokete="$HOME/.local/bin/start-pokete.sh"


# default
test -s ~/.alias && . ~/.alias || true
