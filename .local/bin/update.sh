#!/bin/bash


# Define color variables for formatting
RED='\e[31m'
CYAN='\e[96m'
BLUE='\e[34m'
BLINK='\e[5m'
RA='\e[0m'

# Distroboxe names to upgrade
distrobox_names=('tumbleweed')


# Function to update with zypper
zypper_update() {
    if zypper ref; then
        if ! script -qec "zypper list-updates" /dev/null | tee /dev/tty | grep -q "No updates found"; then
            if script -qec "zypper dup" /dev/null | tee /dev/tty | grep -q "zypper ps -s"; then
                echo -e "${RED}${BLINK}Restart proposed, running processes:${RA}"
                zypper ps -s
            fi
        fi
    else
        echo -e "${RED}ERROR refreshing repositories.${RA}"
    fi
}

# Function to update distroboxes
function distrobox_update() {
    local success=true
    for box in "${@}"; do
        if ! distrobox upgrade "$box"; then
            success=false
            echo -e "${BLUE}_________________________________${RA}"
            echo -e "${CYAN}Failed to update ${RED}$box${RA}"
            echo -e "${BLUE}_________________________________${RA}\n\n"
        fi
    done
}

# Function to update local flatpaks
function user_flatpak_update() {
        flatpak --user update
}

# Function to update system flatpaks
function system_flatpak_update() {
        flatpak --system update
}

# Function to update waybar
function update_waybar() {
        pkill -SIGRTMIN+8 waybar
}

# Function to print separator
function print_seperator() {
        echo -e "\n\n\n${BLUE}_________________________________${RA}"
        echo -e "Now updating ${CYAN}$1${RA}\n\n"
}


# Execute Updates
if [[ $(readlink -f /proc/$(ps -o ppid:1= -p $$)/exe) != $(readlink -f "$SHELL") ]]; then
    	# not a shell
    	export -f zypper_update
    export -f distrobox_update
    export -f user_flatpak_update
    export -f print_seperator
    export -f update_waybar

    export RED
    export CYAN
    export BLUE
    export BLINK
    export RA

    alacritty -e sudo bash -c "export RED='$RED' CYAN='$CYAN' BLUE='$BLUE' BLINK='$BLINK' RA='$RA';
        $(declare -f zypper_update); $(declare -f print_seperator); $(declare -f update_waybar);
        print_seperator 'zypper'; zypper_update; update_waybar; read -p 'Press a button to close'"
	alacritty --hold -e sh -c "print_seperator 'distrobox'; distrobox_update ${distrobox_names[@]}; read -p 'Press a button to close'"
	alacritty -e sh -c 'print_seperator "flatpak"; user_flatpak_update; read -p "Press a button to close"'
else
	# in a shell
        
        print_seperator "zypper" 
        sudo bash -c "$(declare -f zypper_update); zypper_update"
        
        print_seperator "distrobox"
        distrobox_update "${distrobox_names[@]}"

        print_seperator "flatpak"
        user_flatpak_update
fi
