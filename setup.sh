#!/bin/bash

enable_interfaces(){
  #enable spi
  sudo sed -i 's/^dtparam=spi=.*/dtparam=spi=on/' /boot/config.txt
  sudo sed -i 's/^#dtparam=spi=.*/dtparam=spi=on/' /boot/config.txt
  sudo raspi-config nonint do_spi 0
  echo "SPI Interface has been enabled."
  #enable i2c
  sudo sed -i 's/^dtparam=i2c_arm=.*/dtparam=i2c_arm=on/' /boot/config.txt
  sudo sed -i 's/^#dtparam=i2c_arm=.*/dtparam=i2c_arm=on/' /boot/config.txt
  sudo raspi-config nonint do_i2c 0
  echo "I2C Interface has been enabled."
  sed -i '/^dtparam=spi=on/a dtoverlay=spi0-0cs' /boot/firmware/config.txt
}

show_loader() {
  local pid=$!
  local delay=0.1
  local spinstr='|/-\'
  printf "$1 [${spinstr:0:1}] "
  while ps a | awk '{print $1}' | grep -q "${pid}"; do
    local temp=${spinstr#?}
    printf "\r$1 [${temp:0:1}] "
    spinstr=${temp}${spinstr%"${temp}"}
    sleep ${delay}
  done
  if [[ $? -eq 0 ]]; then
    printf "\r$1 [\e[32m\xE2\x9C\x94\e[0m]\n"
  else
    printf "\r$1 [\e[31m\xE2\x9C\x98\e[0m]\n"
  fi
}

# Create the log file
touch "/home/pi/inky/inky-log.txt"

# Define the directory and startup command
currentWorkingDir=$(pwd)
startup_command="cd /home/pi/inky && sudo bash /home/pi/inky/startup.sh > /home/pi/inky/inky-log.txt 2>&1 &"

# Escape the command for sed
escaped_command=$(echo "$startup_command" | sed 's/[\/&]/\\&/g')

# Define start and end markers
start_marker="# BEGIN INKY"
end_marker="# END INKY"

enable_interfaces

echo "Info: Updating rc.local"
# Check if the markers already exist in /etc/rc.local
if grep -q "$start_marker" /etc/rc.local; then
  # Update the command between the markers
  sudo sed -i "/$start_marker/,/$end_marker/c\\$start_marker\n$escaped_command\n$end_marker" /etc/rc.local
  echo "Info: Updated the startup command between markers in /etc/rc.local."
else
  # Add the markers and command before exit 0 if not present
  sudo sed -i "/exit 0/i $start_marker\n$escaped_command\n$end_marker" /etc/rc.local
  echo "Info: Added startup command with markers to /etc/rc.local."
fi

# # Install required pip packages
# echo  "Info: Installing required packages with pip"
# sudo pip install --break-system-packages -r $currentWorkingDir/config/requirements.txt #> /dev/null &
# # show_loader "   Installing packages...   "
# echo  "Info: Packages Installed!"

# # Install inky packages
# echo  "Info: Installing the Pimoroni Inky libraries."
# sudo pip3 install --break-system-packages inky[rpi,example-depends] #> /dev/null &
# sudo pip3 install --break-system-packages inky #> /dev/null &
# # show_loader "   Installing packages...    "
# echo  "Info: Inky package installed!"

# #set up Bonjour
# echo  "Info: Setting up Bonjour"
# sudo apt-get install -y avahi-daemon > /dev/null &
# show_loader "   [1/2] Installing avahi-daemon."
# sudo apt-get install -y netatalk > /dev/null &
# show_loader "   [2/2] Installing netatalk.    "
# echo  "Info: Bonjour set up!"