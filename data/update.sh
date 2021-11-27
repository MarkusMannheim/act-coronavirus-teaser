#!/bin/bash

echo "*** ACT COVID-19 and vaccination update ***"
echo 

git fetch --all
git reset --hard origin/gh-pages

echo

python3 update.py

echo

git add .
git commit -m "update"
git push
