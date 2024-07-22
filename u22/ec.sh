#!/bin/bash

cd
mkdir -p S1LP/img
\cp -r ~/HJS/u22/img/* ~/S1LP/img

# set dark mode and background/wallpaper
echo
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
echo
# echo Set avatar to ~/S1LP/img/eca.jpg with bounding box set to max!
printf "\n\e[1;35m   Set avatar to ~/S1LP/img/eca.jpg with bounding box set to max.\e[0m\n\n"

# EOF
