#!/bin/bash

echo -e "install packages...\n"

echo "updating sudo"
sudo apt update
echo -e "updating complete\n"

echo "installing system packages"
sudo apt install -y libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev libopenjp2-7 libtiff5 libatlas-base-dev vlc python3-pip
echo -e "done\n"

echo "installing pip packages"
pip install pillow luma.lcd RPi.GPIO mutagen python-vlc
echo -e "done\n"

echo "installing packages complete"