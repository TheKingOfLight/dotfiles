#!/bin/bash

entries="Default\nGaming"

selected=$(echo -e $entries|wofi --style $HOME/.config/wofi/Mint-Y-Aqua.css --dmenu --cache-file /dev/null | awk '{print tolower($1)}')

case $selected in
  default)
   exec swaymsg reload;;
  gaming)
    exec swaymsg output DP-1 background $HOME/.local/share/backgrounds/hells-paradise--yamada-fire-with-sword.jpg fill, output DP-1 mode 1920x1080@144Hz, output DP-1 position 1920 0, output DP-1 adaptive_sync on;;
esac
