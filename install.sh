#!/bin/bash

###############################################################################
# Copyright (c) by Z3R0-CDS and Zer0-Industries.com
# All rights reserved.
#
# This script is used to install the application by downloading the appropriate
# executable from GitHub based on the system architecture.
# This script is created by Z3R0-CDS and will be distributed by Z3R0-CDS
# via Github and or Zer0-Industries.com Modifying the code to use it for
# profit is forbidden and will be punished.
###############################################################################

# Global variables for base URL and app name
BASE_URL="https://github.com/Z3R0-CDS/AutoPenguin/releases/latest/download"
APP_NAME="AutoPenguin"

# Function to check the architecture
check_architecture() {
  ARCH=$(uname -m)
  if [[ "$ARCH" == "x86_64" ]]; then
    echo "x86_64"
  elif [[ "$ARCH" == "armv7l" || "$ARCH" == "aarch64" ]]; then
    echo "arm"
  else
    echo "unsupported"
  fi
}

# Function to check the distribution
check_distro() {
  if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO=$ID
  else
    DISTRO=$(uname -s)
  fi
  echo "$DISTRO"
}

# Function to download and install the executable
install_executable() {
  ARCH=$1
  DISTRO=$2
  URL=""

  # Determine the URL based on architecture
  if [[ "$ARCH" == "x86_64" ]]; then
    URL="$BASE_URL/${APP_NAME}-x86_64"
#  elif [[ "$ARCH" == "arm" ]]; then
#    URL="$BASE_URL/${APP_NAME}-arm"
  else
    echo "Unsupported architecture: $ARCH"
    exit 1
  fi

  echo "Downloading from $URL..."
  wget -O "/usr/bin/$APP_NAME" "$URL"

  if [ $? -ne 0 ]; then
    echo "Failed to download the executable."
    exit 1
  fi

  # Make the file executable
#  chmod +x "/usr/bin/$APP_NAME"

  echo "Installation complete. You can now run '$APP_NAME' from the command line."
}

# Main script execution
ARCH=$(check_architecture)
DISTRO=$(check_distro)

echo "Detected architecture: $ARCH"
echo "Detected distribution: $DISTRO"

install_executable "$ARCH" "$DISTRO"
