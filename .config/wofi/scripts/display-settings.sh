#!/bin/bash

entries="Default\nGaming"

selected=$(echo -e $entries|wofi --style $HOME/.config/wofi/Mint-Y-Aqua.css --dmenu --cache-file /dev/null | awk '{print tolower($1)}')

case $selected in
  default)
        exec python3 .config/sway/dispaly/display_setting.py default;;
  gaming)
        exec python3 .config/sway/display/display_setting.py gaming;;
esac
