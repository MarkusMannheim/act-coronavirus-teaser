@ECHO off
TITLE ACT COVID-19 data update
ECHO Scraping ACT Health COVID-19 data ...
start py ./scrape.py
ECHO Recording changes ...
ECHO.
git add ..\*.*
git commit -m "scheduled update"
git push
ECHO.
ECHO Update complete
exit