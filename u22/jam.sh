#!/bin/bash

jamlog="$@"
jamt=$(date +%s)
jamhex=$(printf "%x" $jamt)
echo Writing to file...
echo $jamhex $jamlog >> ~/jam.info

# EOF
