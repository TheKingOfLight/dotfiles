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

# ls
alias ls="ls --color=auto"
alias ls.="ls -d .* --color=auto"

# zypper/flatpak/yast
alias zypper="sudo zypper"
alias appinfo="\zypper info"
alias appsearch="\zypper search"
alias update="sudo \zypper ref && sudo \zypper dup && flatpak update && distrobox-upgrade --all"

alias flatpak="flatpak --user"

alias yast="su -c 'yast --qt'"


# default
test -s ~/.alias && . ~/.alias || true
