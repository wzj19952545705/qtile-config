#!/bin/fish
lxsession&
#feh --bg-scale ~/Pictures/WallPapers/parrot.jpg&
/home/wzj/.fehbg&
picom&
fcitx5&
copyq&
/usr/bin/emacs --daemon&
nm-applet&
xidlehook --not-when-fullscreen --timer 360 "xrandr --output $PRIMARY_DISPLAY --brightness .6" "xrandr --output $PRIMARY_DISPLAY --brightness 1" --timer 360 "xrandr --output $PRIMARY_DISPLAY --brightness 1;systemctl suspend" "slock"&
