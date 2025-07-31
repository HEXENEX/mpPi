#!/bin/bash

echo -e "installing packages...\n"

echo "updating sudo"
sudo apt update
echo -e "updating complete\n"

echo "installing system packages"
sudo apt install -y libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev libopenjp2-7 libatlas-base-dev vlc python3-pillow python3-rpi.gpio
echo -e "done\n"

echo "installing pip packages"
pip3 install luma.lcd mutagen python-vlc
echo -e "done\n"

echo "installing packages complete"