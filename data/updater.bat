@ECHO off
TITLE ACT COVID-19 update
ECHO Commencing scrape ...
start /w /b py ./data.py
ECHO.
ECHO Recording changes ...
ECHO.
git add .
git commit -m "scheduled update"
git push
ECHO.
ECHO Update complete
exit