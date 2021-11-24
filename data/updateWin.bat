@echo off
title "COVID-19 case and vaccination update"

@echo Starting COVID-19 case and vaccination update ...

git fetch --all
git reset --hard origin/gh-pages

py updateWin.py
