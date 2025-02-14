#!/bin/basdh

mydate=$1
echo Converting $mydate...
decimal=$(echo $((16#$mydate)))
date -u -d +@$decimal
date -d +@$decimal

# EOF
