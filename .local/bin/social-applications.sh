#!/bin/bash

#
#________________________________________________________________
#________________________________________________________________
#
# Open desired social application on predefined workspace
# Vers. 0.0.3
# Author: King of the light
# License: Unlicense
#
#________________________________________________________________
#________________________________________________________________
#

# Define workspace and mode
ws="8"
mode="tabbed"

# Switch to workspace 
swaymsg workspace $ws

# Open application 
element-desktop &
distrobox-enter  -n tumbleweed -- /bin/sh -l -c  armcord &
thunderbird &
distrobox-enter  -n tumbleweed -- /bin/sh -l -c  "signal-desktop --use-tray-icon" %U &

# Set Mode
swaymsg layout $mode

