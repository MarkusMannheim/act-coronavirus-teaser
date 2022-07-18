#!/bin/bash

echo "Starting ACT COVID-19 update ..."
echo

git fetch --all
git reset --hard origin/gh-pages

echo

python3 update.py

echo

git add .
git commit -m "update"
git push
