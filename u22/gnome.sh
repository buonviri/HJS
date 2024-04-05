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
    gsettings set org.gnome.desktop.session idle-delay 900
    gsettings get org.gnome.desktop.session idle-delay
else
    gsettings set org.gnome.desktop.interface color-scheme 'prefer-light'
    gsettings get org.gnome.desktop.interface color-scheme
    gsettings set org.gnome.desktop.background picture-uri file:///home/ec/HJS/u22/white.png
    gsettings get org.gnome.desktop.background picture-uri
    # gsettings set org.gnome.desktop.background picture-uri-dark file:///home/ec/HJS/u22/white.png
    # gsettings get org.gnome.desktop.background picture-uri-dark
    gsettings set org.gnome.desktop.session idle-delay 900
    gsettings get org.gnome.desktop.session idle-delay
fi

echo
echo Setup complete.

# EOF
