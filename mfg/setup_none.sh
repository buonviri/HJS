#!/bin/bash

MOD="pcie_sakura"
DAEMON="ec_daemon"

#
# compile the driver
#
if cd driver && make && cd ..; then
  echo "Module '${MOD}' compiled"
else
  echo "Cannot compile module '${MOD}'"
  exit 1
fi

#
# load the driver
#
if lsmod | grep -q "^${MOD}"; then
  echo "Module '${MOD}' already loaded"
else
  echo "Module '${MOD}' not loaded. Loading..."
  if sudo insmod "driver/$MOD.ko"; then
    echo "Module '${MOD}' loaded"
  else
    echo "Cannot load module '${MOD}'"
    exit 1
  fi
fi

#
# setting device permissions
#
if sudo chmod 666 /dev/sakura_pcie*; then
  echo "Permissions for device driver files set"
else
  echo "Error setting permissions'"
  exit 1
fi

#
# start the EC daemon
#
daemon_running() {
  pgrep -f "$DAEMON" > /dev/null 2>&1
}
if daemon_running; then
  echo "Daemon is already running"
else
  echo "Daemon '$DAEMON' not running. Starting..."
  eval "sudo -b ./$DAEMON"
  sleep 2
  if daemon_running; then
    echo "Daemon started"
  else
    echo "Cannot start daemon"
    exit 1
  fi
fi

#
# perform the DMA speed test
# removed by HJS
#if ./dma_test; then
#  echo "DMA test finished"
#else
#  echo "Error running the DMA test'"
#  exit 1
#fi

echo "SAKURA II board initialized correctly"
echo "SETUP DONE"
exit 0
