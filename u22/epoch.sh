#!/bin/basdh

mydate=$1
echo Converting $mydate...
decimal=$(printf "%x" "$mydate")
date -u -d +@$decimal

# EOF
