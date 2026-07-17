@echo off
REM Double-click to run the Content Studio as a local web app on THIS machine.
REM It serves the studio AND powers the "Generate" buttons (they shell out to the
REM render scripts locally). LOCAL ONLY - do not tunnel/forward port 8092.
cd /d "%~dp0"
echo ============================================================
echo   Carrie - Content Studio (local)
echo   Open in your browser:  http://127.0.0.1:8092/studio/
echo   Keep this window open while you work. Close it to stop.
echo ============================================================
start "" "http://127.0.0.1:8092/studio/"
python build\studio_app.py
pause
