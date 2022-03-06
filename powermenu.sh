#!/bin/fish

set option (echo "Log out"\n"Suspend"\n"Power off"\n"Reboot" | rofi -dmenu -p "PowerMenu>")

switch $option
	case "Suspend"
		systemctl suspend
	case "Power off"
		poweroff
	case "Reboot"
		reboot
	case "Log out"
		loginctl kill-session $XDG_SESSION_ID
end
