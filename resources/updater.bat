@ECHO off
TITLE ACT COVID-19 data update
ECHO Scraping ACT Health COVID-19 data ...
start /b /wait py -m ./scrape.py
git add ..\*.*
git commit -m "scheduled update"
git push
