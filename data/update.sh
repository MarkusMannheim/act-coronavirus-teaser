@echo off
title "COVID-19 case and vaccination update"

@echo Starting COVID-19 case and vaccination update ...
@echo.

git fetch --all
git reset --hard origin/gh-pages

@echo.
py updateWin.py

@echo.
git add .
git commit -m "update"
git push
