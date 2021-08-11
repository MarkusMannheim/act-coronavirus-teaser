@ECHO off
TITLE ACT COVID-19 update
ECHO Resetting data ...
git fetch --all
git reset --hard origin/gh-pages
ECHO.
ECHO Commencing scrape ...
start /w /b py ./check_act.py
ECHO.
start /w /b py ./check_federal.py
ECHO.
ECHO Recording changes ...
ECHO.
cd ..
git add .
git commit -m "scheduled update"
git push
ECHO.
ECHO Update complete
exit