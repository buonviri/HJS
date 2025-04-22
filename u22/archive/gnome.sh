#!/bin/bash

read -p 'Hit d or <Enter> to select dark mode... ' -n 1 -r
echo
ascii_value=$(printf "%d" "'$REPLY")
echo # "$ascii_value"
if [[ "$ascii_value" -eq 100 || "$ascii_value" -eq 68 || "$ascii_value" -eq 0 ]]
then
    gsettings set org.gnome.desktop.interface color-scheme 'prefer-dark'
    gsettings get org.gnome.desktop.interface color-scheme
    # gsettings set org.gnome.desktop.background picture-uri file:///home/ec/HJS/u22/black.png
    # gsettings get org.gnome.desktop.background picture-uri
    gsettings set org.gnome.desktop.background picture-uri-dark file:///home/ec/HJS/u22/black.png
    gsettings get org.gnome.desktop.background picture-uri-dark
else
    gsettings set org.gnome.desktop.interface color-scheme 'prefer-light'
    gsettings get org.gnome.desktop.interface color-scheme
    gsettings set org.gnome.desktop.background picture-uri file:///home/ec/HJS/u22/white.png
    gsettings get org.gnome.desktop.background picture-uri
    # gsettings set org.gnome.desktop.background picture-uri-dark file:///home/ec/HJS/u22/white.png
    # gsettings get org.gnome.desktop.background picture-uri-dark
fi

# set screen timeout
gsettings set org.gnome.desktop.session idle-delay 3600
gsettings get org.gnome.desktop.session idle-delay

# remove trash, note that older versions require .extensions.desktop-icons instead
gsettings set org.gnome.shell.extensions.ding show-trash false
gsettings get org.gnome.shell.extensions.ding show-trash

# remove home, note that older versions require .extensions.desktop-icons instead
gsettings set org.gnome.shell.extensions.ding show-home false
gsettings get org.gnome.shell.extensions.ding show-home

echo
echo Setup complete. Sincerely, HJS

# EOF
