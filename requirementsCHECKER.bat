@echo off
echo ==========================================
echo   MIS380 Dashboard Environment Check
echo ==========================================

:: --- Check Python ---
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python is NOT installed.
    echo Download it from https://www.python.org/downloads/
    echo ==========================================
    pause
    exit /b
) ELSE (
    for /f "tokens=2 delims= " %%a in ('python --version') do set pyver=%%a
    echo Python is installed: %pyver%
)

:: --- Check pip ---
pip --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo pip not found. Try reinstalling Python and make sure "Add to PATH" is checked.
) ELSE (
    echo pip is installed.
)

:: --- Check Flask ---
python -c "import flask" >nul 2>&1
IF ERRORLEVEL 1 (
    echo Flask not installed. Run: pip install Flask
) ELSE (
    echo Flask is installed.
)

:: --- Check pipenv ---
python -c "import pipenv" >nul 2>&1
IF ERRORLEVEL 1 (
    echo pipenv not installed (optional). Run: pip install --user pipenv
) ELSE (
    echo pipenv is installed.
)

echo ==========================================
echo Environment check complete.
echo Run: python app.py
echo ==========================================
pause
