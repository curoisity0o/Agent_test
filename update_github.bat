@echo off
cd /d d:\code\LLM\Agent_test
git config user.email "curoisity0o@users.noreply.github.com"
git config user.name "curoisity0o"
git add .
git status
echo.
echo Press any key to commit and push...
pause >nul
git commit -m "Update: Add project summary and cleanup"
git push
echo.
echo Done! Press any key to exit...
pause >nul
