#!/bin/bash

cd
mkdir -p S1LP/img
echo copy file to img using \cp -r /zzz/zzz/* /xxx/xxx

gsettings set org.gnome.desktop.interface color-scheme 'prefer-dark'
gsettings get org.gnome.desktop.interface color-scheme
gsettings set org.gnome.desktop.background picture-uri-dark file:///home/ec/S1LP/img/ecw.png
gsettings get org.gnome.desktop.background picture-uri-dark

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
