#!/bin/sh
xrandr --output DisplayPort-0 --mode 1920x1080 --rate 144 &
feh --bg-scale ~/Pictures/blue-firewatch.jpg &
picom -b --config ~/.config/picom.conf 
dunst &
nm-applet --sm-disable &
