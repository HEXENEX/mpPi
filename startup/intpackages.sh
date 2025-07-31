#!/bin/bash

echo "install packages..."

echo "installing pip packages"
pip install pillow luma.lcd RPi.GPIO mutagen python-vlc
echo "done"

echo "installing system packages"
sudo apt install libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev libopenjp2-7 libtiff5 libatlas-base-dev vlc
echo "done"

echo "installing packages complete"