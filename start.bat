@echo off
setlocal
cd /d "%~dp0"

set "VENV_DIR=%~dp0.venv"
set "PYTHON=%VENV_DIR%\Scripts\python.exe"
set "DEPS_MARKER=%VENV_DIR%\.dependencies-installed"

echo ========================================
echo        4x GAN Image Upscaler
echo ========================================
echo.

REM Check that the trained model exists
if not exist "%~dp0checkpoint_gan_epoch_600.pth" (
    echo ERROR: Model checkpoint not found.
    echo Place checkpoint_gan_epoch_600.pth in this folder.
    pause
    exit /b 1
)

REM Create the local virtual environment only if missing
if not exist "%PYTHON%" (
    echo Creating project-local Python environment...

    where py >nul 2>&1
    if not errorlevel 1 (
        py -3.11 -m venv "%VENV_DIR%"
    )

    if errorlevel 1 (
        python -m venv "%VENV_DIR%"
    )

    if errorlevel 1 goto setup_error
)

REM Install dependencies on first launch
if not exist "%DEPS_MARKER%" (
    echo Installing dependencies. This may take a while...
    "%PYTHON%" -m pip install --upgrade pip
    if errorlevel 1 goto setup_error

    "%PYTHON%" -m pip install -r "%~dp0requirements.txt"
    if errorlevel 1 goto setup_error

    type nul > "%DEPS_MARKER%"
)

REM Reuse an already-running application
curl -s http://127.0.0.1:8000/ >nul 2>&1
if not errorlevel 1 goto ready

REM Start the API server
echo.
echo Starting the application...

start "" /B "%PYTHON%" -m uvicorn app:app --host 127.0.0.1 --port 8000

REM Wait up to 60 seconds for the API
set /a attempts=0

:wait
timeout /t 1 /nobreak >nul
curl -s http://127.0.0.1:8000/ >nul 2>&1
if not errorlevel 1 goto ready

set /a attempts+=1
if %attempts% geq 60 goto server_error
goto wait

:ready
echo Application is ready!
start "" http://127.0.0.1:8000/app
exit /b 0

:setup_error
echo.
echo ERROR: Python environment setup failed.
echo Check that Python 3.11 and requirements.txt are available.
pause
exit /b 1

:server_error
echo.
echo ERROR: The API did not respond within 60 seconds.
echo Check the port, dependencies, and app.py for errors.
pause
exit /b 1