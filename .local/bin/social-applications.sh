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
element-desktop --enable-features=UseOzonePlatform --ozone-platform=wayland &
distrobox-enter  -n tumbleweed -- /bin/sh -l -c  'armcord --enable-features=UseOzonePlatform --ozone-platform=wayland' &
thunderbird &
distrobox-enter  -n tumbleweed -- /bin/sh -l -c  "signal-desktop --use-tray-icon --enable-features=UseOzonePlatform --ozone-platform=wayland " %U &

# Set Mode
swaymsg layout $mode
