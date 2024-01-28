#!/bin/bash

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

