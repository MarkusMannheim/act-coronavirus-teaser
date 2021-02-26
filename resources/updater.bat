@ECHO off
TITLE ACT COVID-19 data update
ECHO Scraping ACT Health COVID-19 data ...
start /w /b py ./scrape.py
ECHO Recording changes ...
git add ..\*.*
git commit -m "scheduled update"
git push
ECHO
ECHO Update complete
exit