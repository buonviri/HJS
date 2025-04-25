
# Start of EdgeCortix .bashrc

# remove default aliases
unalias l
unalias ll
unalias la
unalias alert
unalias egrep
unalias fgrep

# Print "ubuntu" to terminal screen on startup, with rev
echo "        _                 _         "
echo "  _   _| |__  _   _ _ __ | |_ _   _ "
echo " | | | | '_ \| | | | '_ \| __| | | |"
echo " | |_| | |_) | |_| | | | | |_| |_| | by HJS"
echo "  \__,_|_.__/ \__,_|_| |_|\__|\__,_| 0x0006"
echo

if [ -e ~/.auto_prodtest ]; then  # check if file exists
  uptime=$(date -d "`cut -f1 -d. /proc/uptime` seconds ago" -u)  # get boot timestamp
  cat ~/.auto_prodtest | grep "$uptime" > /dev/null  # check grep, discard result
  if [ $? -eq 0 ]; then  # grep match
    echo "[Skipping auto-prodtest]"
    echo  # newline before prompt
  else
    echo "$uptime" > ~/.auto_prodtest  # write boot time to auto file
    echo "[Starting auto-prodtest, disable with pt-, CTRL-C twice to skip]"
    echo  # newline before sudo entry
    pt  # prodtest
  fi
fi

# EOF






# MOAR
