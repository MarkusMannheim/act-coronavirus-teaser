START /B /wait node .\scrape.js
START /B git add ..\*.*
START /B git commit -m "scheduled update"
START /B git push
