#
#________________________________________________________________
#________________________________________________________________
#
# .bashrc
# bash main config file
# Vers. 0.0.2
# Author: King of the light
# License: GNU General Public License v3.0
#
#________________________________________________________________
#________________________________________________________________
#




#
#________________________________________________________________
# Imports
#

# Import alias from file
test -s ~/.alias && . ~/.alias || true
test -s ~/.alias-private && . ~/.alias-private || true


#
#________________________________________________________________
# Run !always! at startup
#

# Short neofetch (from alias --> cat)
neofetch short

[ -f "/home/light/.ghcup/env" ] && source "/home/light/.ghcup/env" # ghcup-env
