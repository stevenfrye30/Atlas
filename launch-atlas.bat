@echo off
setlocal

REM ATLAS one-click launcher (Windows)
REM
REM What this does:
REM   1. Moves to the project folder.
REM   2. Builds the site by running scripts\build.py.
REM   3. Opens your default browser to http://localhost:8000.
REM   4. Starts a local web server in this window.
REM
REM How to stop:
REM   Press Ctrl+C in this window, or close the window.

REM Move to the folder containing this batch file (the project root).
cd /d "%~dp0"

REM ---- Check that Python is installed and on the PATH. ----
where python >nul 2>&1
if errorlevel 1 (
    echo.
    echo Python was not found on this computer.
    echo.
    echo Install Python 3.8 or later from:
    echo     https://www.python.org/downloads/
    echo.
    echo During installation, check the box "Add Python to PATH".
    echo Then close this window and double-click launch-atlas.bat again.
    echo.
    pause
    exit /b 1
)

REM ---- Build the site. ----
echo.
echo Building ATLAS...
echo.
python scripts\build.py
if errorlevel 1 (
    echo.
    echo Build failed. See the message above for the specific problem.
    echo Fix the file it names, then double-click launch-atlas.bat again.
    echo.
    pause
    exit /b 1
)

REM ---- Open the browser, then start the server. ----
echo.
echo Opening browser at http://localhost:8000 ...
echo Press Ctrl+C in this window to stop the server.
echo.

REM The browser opens first; the server starts a moment later.
REM If the browser loads before the server is ready, just refresh the page.
start "" "http://localhost:8000"

REM Start the local server. It runs until you stop it.
REM If port 8000 is already in use, Python will print an error here
REM ("OSError: [WinError 10048]..."). Close whatever else is using
REM port 8000, or edit this file to use a different port.
python -m http.server 8000 --directory docs

echo.
pause
