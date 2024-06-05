#!/bin/sh
xrandr --output DisplayPort-0 --mode 1920x1080 --rate 240 &
feh --bg-scale ~/Pictures/blue-firewatch.jpg &
picom -b -f --config ~/.config/picom.conf 
dunst &
nm-applet --sm-disable &
