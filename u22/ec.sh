#!/bin/bash

cd
mkdir -p S1LP/img  # -p creates parents and doesn't fail if some already exist
mkdir -p S2LP/img  # -p creates parents and doesn't fail if some already exist
mkdir -p S2M2/img  # -p creates parents and doesn't fail if some already exist
mkdir -p EC/img    # -p creates parents and doesn't fail if some already exist
\cp -r ~/HJS/u22/img/* ~/EC/img  # slash uses non-alias version, -r is recursive
# mkdir -p S1LP-847  # test, no longer needed

# set dark mode and background/wallpaper
# echo  # removed for a.sh script
echo dark mode and background:
gsettings set org.gnome.desktop.interface color-scheme 'prefer-dark'
gsettings get org.gnome.desktop.interface color-scheme
gsettings set org.gnome.desktop.background picture-uri-dark file:///home/ec/S1LP/img/ecw.png
gsettings get org.gnome.desktop.background picture-uri-dark

# set screen timeout
echo
echo screen timeout and desktop icons:
gsettings set org.gnome.desktop.session idle-delay 3600
gsettings get org.gnome.desktop.session idle-delay
# remove trash, note that older versions require .extensions.desktop-icons instead
gsettings set org.gnome.shell.extensions.ding show-trash false
gsettings get org.gnome.shell.extensions.ding show-trash
# remove home, note that older versions require .extensions.desktop-icons instead
gsettings set org.gnome.shell.extensions.ding show-home false
gsettings get org.gnome.shell.extensions.ding show-home

# set performance mode
echo
echo power profile:
powerprofilesctl set performance
powerprofilesctl get

cd "$OLDPWD"

echo
echo Setup complete. Sincerely, HJS
# echo Set avatar to ~/S1LP/img/eca.jpg with bounding box set to max!
printf "\n\e[1;35m  Set avatar to ~/S1LP/img/eca.jpg with bounding box set to max.\e[0m\n\n"

# EOF
