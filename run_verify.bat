@echo off
cd /d "%~dp0"
"venv\Scripts\python.exe" verify_week0.py
echo Exit code: %ERRORLEVEL%
pause
