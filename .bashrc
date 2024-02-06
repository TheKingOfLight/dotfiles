#
#________________________________________________________________
#________________________________________________________________
#
#.bashrc
# bash main config file
# Vers. 0.0.1
# Author: King of the light
# License: GNU General Public License v3.0
#
#________________________________________________________________
#________________________________________________________________
#




#
#________________________________________________________________
# Custom alias
#

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


#
#________________________________________________________________
# Additional settings
#

# import alias from file
test -s ~/.alias && . ~/.alias || true
