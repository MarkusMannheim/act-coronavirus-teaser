echo on
Scraping ACT Health COVID-19 data
echo off
START /B /wait node .\scrape.js
START /B git add ..\*.*
START /B git commit -m "scheduled update"
START /B git push
more
