@echo off
cd /d d:\code\LLM\Agent_test
git config user.email "curoisity0o@users.noreply.github.com"
git config user.name "curoisity0o"
git add .
git commit -m "Initial commit: Agent project with ReAct mode"
git branch -M main
git remote remove origin 2>nul
git remote add origin https://github.com/curoisity0o/Agent_test.git
git push -u origin main
pause
