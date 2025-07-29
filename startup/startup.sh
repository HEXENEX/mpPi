#!/bin/bash
echo "startup sequence starting..."

echo "pulling repository"
cd startup
python3 pullrequest.py
cd ..

git fetch origin
git reset --hard origin/main

echo "running mpPi UI"
python3 main.py