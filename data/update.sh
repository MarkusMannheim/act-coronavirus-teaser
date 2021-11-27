#!/bin/bash

echo "ACT COVID-19 and vaccination update beginning"
echo 

git fetch --all
git reset --hard origin/gh-pages

echo

python3 update.py
