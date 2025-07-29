#!/bin/bash
echo "startup sequence starting..."

echo "pulling repository"
python3 startup/pullrequest.py &
git pull

echo "running mpPi UI"
python3 main.py