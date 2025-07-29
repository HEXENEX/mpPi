#!/bin/bash
echo "startup sequence starting..."

echo "pulling repository"
cd startup
python3 pullrequest.py &

git fetch origin
git reset --hard origin/main

cd ..
echo "running mpPi UI"
python3 main.py