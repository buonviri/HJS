# remove default aliases
unalias l
unalias ll
unalias la
unalias alert
unalias egrep
unalias fgrep

# temporary alias to run antonio's dna2 script
alias ant='cd ~/S2LP/dna2_self_test && ./setup.sh ; echo ; echo Ensure that compute blocks 01 and 02 are enabled, then ./run.sh or ./run.sh 999'
alias ant22='cd ~/S2LP/dna2_self_test_2_2_0 && ./setup_3pg.sh ; echo ; echo Ensure that compute blocks 01 and 02 are enabled, then ./run_3pg.sh or ./run_3pg.sh 999'
alias varsakura='cat /var/log/syslog | grep -a -i sakura'

# Print "ubuntu" to terminal screen on startup
echo "        _                 _         "
echo "  _   _| |__  _   _ _ __ | |_ _   _ "
echo " | | | | '_ \| | | | '_ \| __| | | |"
echo " | |_| | |_) | |_| | | | | |_| |_| |"
echo "  \__,_|_.__/ \__,_|_| |_|\__|\__,_|"
echo

# EOF
