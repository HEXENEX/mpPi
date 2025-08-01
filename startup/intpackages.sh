#!/bin/bash

echo -e "installing packages...\n"

echo "updating sudo"
sudo apt update
echo -e "updating complete\n"

echo "installing python3"
sudo apt install -y python3
echo -e "python3 install complete\n"

echo "installing system packages"
# more packages will be added in the future, i dont know which ones i need
sudo apt install -y  python3-vlc python3-pil python3-rpi.gpio python3-luma.lcd python3-mutagen bluez-alsa-utils bluez-tools pulseaudio-module-bluetooth
echo -e "system packages install complete\n"

echo "all packages installed"