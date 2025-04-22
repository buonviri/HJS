#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Usage: epoch [hextimestamp]"
else
  mydate=$1
  echo Converting $mydate...
  decimal=$(echo $((16#$mydate)))
  date -u -d +@$decimal  # UTC
  date -d +@$decimal  # local time
fi

# EOF
