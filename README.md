# AutoPenguin

## About
    Aimed to provide a automatic setup for any linux maschine
    It is not tested on ARM or any OS other than arch/fedora based distros.
    My daily driver is Cachy OS so most stuff is tested on there.
    I also will use it on Fedora from time to time.
    Primary use is for me so modifications might be usefull.

## Disclaimer
    EARLY DEVELOPMENT! FEATURES ARE MISSING!
    DOES NOT SUPPORT WINDOWS! Includes the migration too!
    It is meant to setup one linux system to the other!

    A Version is finished if you can download it via the Release tab.

## Installation

    wget -O install.sh https://raw.githubusercontent.com/Z3R0-CDS/AutoPenguin/main/install.sh
    chmod +x install.sh
    sudo ./install.sh

    or 
  
    wget -O install.sh https://raw.githubusercontent.com/Z3R0-CDS/AutoPenguin/main/install.sh
    chmod +x install.sh
    *edit the install.sh INSTALL_DIR to some other pass that isn't roots*
    ./install.sh

    or 
    
    use source or even build the application from source using executable.sh
    this will require pip, pyinstaller and a venv is recommended!

## Usage

    Will be finished soon!

    1. Start the cli interface. Type "AutoPenguin"

## Features
- Auto save to config
- SCP copy from remote
- Version checks
- Updater
- sys commands passthrough
- Privacy and Simple mode
- Built in help command
- Custom setup scripts

## Technology stack

Installer
- Shell script
  - Curl
  - Requires sudo to get write rights for /usr/bin/

AutoPenguin
- Python 3.12 +/-
  - getpass
  - os
  - sys
  - time
  - json
  - colorama
  - readline
  - requests
  - packaging

## Limitations and Copyright

    This script is created by Z3R0-CDS and will be distributed by Z3R0-CDS
    via Github and/or Zer0-Industries.com. Modifying the code to use it for
    profit is forbidden and will be punished.
    Questions? Contact copyright@zer0-industries.com
