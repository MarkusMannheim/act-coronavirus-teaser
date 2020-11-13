@ECHO off
TITLE ACT COVID-19 data update
ECHO Scraping ACT Health COVID-19 data ...
start /b /wait py ./scrape.py
git add ..\*.*
git commit -m "scheduled update"
git push
timeout 2 >nul
exit