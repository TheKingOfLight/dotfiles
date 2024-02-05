#!/bin/bash

entries="Default\nGaming"

selected=$(echo -e $entries|wofi --style $HOME/.config/wofi/Mint-Y-Aqua.css --dmenu --cache-file /dev/null | awk '{print tolower($1)}')

case $selected in
  default)
        exec sh .local/bin/display-setting.sh default;
  gaming)
        exec sh .local/bin/display-setting.sh gaming;
esac
