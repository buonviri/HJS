#!/bin/bash

# determine wait timer
if [ $# == 1 ]; then  # one arg was passed
  delay="$1"  # set to arg
else
  delay="4000"  # default is four seconds
fi

function purple () {
  printf "\e[1;35m%b\e[0m" "$1"
}

# initial warning
echo
purple "This process may take a while. Do not access the serial port until it completes.\n"
echo

# set up picocom
picocom -qrX -b 115200 --flow x --send-cmd ascii-xfr /dev/ttyUSB0  # q = quiet, r = no-reset, X = exit immediately 

# send bist command, wait up to [delay] seconds for more data
echo "Delay = $delay"
echo "bist all errstop -n 99" | picocom -qrix $delay /dev/ttyUSB0  # q = quiet, r = no-reset, i = no-init, x = exit after [delay]

# hopefully it finished!
purple "Done. -HJS\n"
echo

# End

# bist [a|b|ab|a0|a1|b0|b1|all] [mode] [test] [errstop] [-n 999] [-a 0x123]
# 
# Run DDR BIST now:
#     Use A, B, or AB to test both ddr0 and ddr1.
#     Use a0, a1, b0, or b1 to test ddr0 on A, ddr1 on A, etc.
#     Use ALL to test A0, A1, B0, B1.
# 
#     [mode] is ctlr or pi.
# 
#     [test] is addr or data.
# 
#     [errstop] stops iterating when an error is encountered; otherwise BIST runs
#     all n iterations.
# 
#     [-n 999] specifies the iteration count. The default is 1. The maximum value
#     is 0xffffffff.
# 
#     [-a 0xNNN] specifies the address space used for the test; a missing
#     value or a value of 0 selects the default address space.
