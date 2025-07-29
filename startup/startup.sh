#!/bin/bash
echo "startup sequence starting..."

echo "pulling repository"
python3 startup/pullrequest.py &
git fetch origin
git reset --hard origin/main

echo "running mpPi UI"
python3 main.py