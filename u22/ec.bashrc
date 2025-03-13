
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
echo "  \__,_|_.__/ \__,_|_| |_|\__|\__,_| 0x0003"
echo

if [ -e ~/.auto_prodtest ]; then  # check if regular file exists
  prodtest
else
  echo "[Enable auto-prodtest with pt+]"
  echo
fi

# EOF






# MOAR
