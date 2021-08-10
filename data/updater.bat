@ECHO off
TITLE ACT COVID-19 update
ECHO Commencing scrape ...
ECHO.
start /w /b py ./data.py
ECHO Recording changes ...
ECHO.
git add .
git commit -m "scheduled update"
git push
ECHO.
ECHO Update complete
exit