#!/bin/bash
echo "startup"

echo "pulling repository"
git pull

echo "running mpPi UI"
python3 main.py