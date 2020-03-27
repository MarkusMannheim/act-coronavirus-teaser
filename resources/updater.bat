@ECHO OFF
ECHO Welcome to Markus's ACT coronavirus updater!
node
node .\scrape.js
git add ..
git commit -m "scheduled update"
git push
PAUSE
