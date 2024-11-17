#!/bin/bash

pid=$(lsof -i :80| awk '/python/ { pid=$2 } END { print pid }')
currentDir=$(pwd)
currentFolder=${PWD##*/} 

# do a sudo check!
if [ "$EUID" -ne 0 ]; then
  echo "ERROR: Inky start script requires root privileges. Please run it with sudo."
  exit 1
fi

if [[ -z $pid ]]; then
  echo "Info: No process found using port 80!"
else
  echo "Info: Found PID using port 80: $pid."
  echo "Info: Killing process $pid..."
  if sudo kill -9 "$pid" >/dev/null 2>&1; then
    echo "Info: Process killed!"
  else
    echo "Error: Failed to kill process $pid."
  fi
fi

echo "Info: Starting Inky!"

sudo python -u $currentDir/src/inky_runner.py