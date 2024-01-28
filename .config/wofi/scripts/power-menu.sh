#!/bin/bash

entries="⏻ Shutdown\n⭮ Reboot\n⏾⇠ Logout\n🔒 Lock\n- Suspend"

selected=$(echo -e $entries|wofi --config $HOME/.config/wofi/config --style $HOME/.config/wofi/Mint-Y-Aqua.css --dmenu --cache-file /dev/null | awk '{print tolower($2)}')

case $selected in
  shutdown)
    exec systemctl poweroff -i;;
  reboot)
    exec systemctl reboot;;
  logout)
    swaymsg exit;;
  lock)
    exec swaylock;;
  suspend)
    exec systemctl suspend;;
esac
