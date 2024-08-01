#!/bin/bash

###############################################################################
# Copyright (c) by Z3R0-CDS and Zer0-Industries.com
# All rights reserved.
#
# This script is created by Z3R0-CDS and will be distributed by Z3R0-CDS
# via Github and/or Zer0-Industries.com. Modifying the code to use it for
# profit is forbidden and will be punished.
###############################################################################

# Global variables for repository and app name
REPO="Z3R0-CDS/AutoPenguin"
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

# Function to get the latest release tag from GitHub
get_latest_release() {
  LATEST_RELEASE=$(curl --silent "https://api.github.com/repos/$REPO/releases/latest")

  # Extract the tag_name using grep, sed, and awk
  TAG=$(echo "$LATEST_RELEASE" | grep '"tag_name":' | sed -E 's/.*"tag_name":\s*"([^"]+)".*/\1/')

  if [ -z "$TAG" ]; then
    echo "Failed to fetch the latest release tag. Response from GitHub API:"
    echo "$LATEST_RELEASE"
    exit 1
  fi

  echo "$TAG"
}

# Function to download and install the executable
install_executable() {
  ARCH=$1
  TAG=$2
  URL=""

  # Determine the URL based on architecture and tag
  if [[ "$ARCH" == "x86_64" ]]; then
    URL="https://github.com/$REPO/releases/download/$TAG/${APP_NAME}-x86_64"
  elif [[ "$ARCH" == "arm" ]]; then
    URL="https://github.com/$REPO/releases/download/$TAG/${APP_NAME}-arm"
  else
    echo "Unsupported architecture: $ARCH"
    exit 1
  fi

  echo "Downloading from $URL..."
  #wget -O "/usr/bin/$APP_NAME" "$URL"
  curl -sL "$URL" -o "/usr/bin/$APP_NAME"

  if [ $? -ne 0 ]; then
    echo "Failed to download the executable."
    exit 1
  fi

  # Make the file executable
  chmod +x "/usr/bin/$APP_NAME"

  echo "Installation complete. You can now run '$APP_NAME' from the command line."
}

# Main script execution
ARCH=$(check_architecture)
TAG=$(get_latest_release)

echo "Detected architecture: $ARCH"
echo "Latest release tag: $TAG"

install_executable "$ARCH" "$TAG"
