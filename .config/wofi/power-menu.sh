#!/bin/bash

entries="⏻ Shutdown\n⭮ Reboot\n⏾⇠ Logout\n Lock\n Suspend"

selected=$(echo -e $entries|wofi --width 300 --height 210 --dmenu --cache-file /dev/null | awk '{print tolower($2)}')

case $selected in
  shutdown)
    exec systemctl poweroff -i;;
  reboot)
    exec systemctl reboot;;
  logout)
    swaymsg exit;;
  lock)
    exec "swaylock -f -c 000000";;
  suspend)
    exec systemctl suspend;;
esac
