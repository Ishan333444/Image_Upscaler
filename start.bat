```bat
@echo off
setlocal
cd /d "%~dp0"

set "VENV_DIR=%~dp0.venv"
set "PYTHON=%VENV_DIR%\Scripts\python.exe"
set "DEPS_MARKER=%VENV_DIR%\.dependencies-installed"
set "MODEL_FILE=%~dp0checkpoint_gan_epoch_600.pth"
set "MODEL_URL=https://huggingface.co/coolknifer333444/image-upscaler-gan/resolve/main/checkpoint_gan_epoch_600.pth"

echo ========================================
echo        4x GAN Image Upscaler
echo ========================================
echo.

REM Download the model checkpoint if missing
if not exist "%MODEL_FILE%" (
    echo Model checkpoint not found.
    echo Downloading from Hugging Face...
    echo This may take a few minutes.
    echo.

    powershell -NoProfile -ExecutionPolicy Bypass -Command "try { Invoke-WebRequest -Uri '%MODEL_URL%' -OutFile '%MODEL_FILE%' -ErrorAction Stop; exit 0 } catch { Write-Host $_.Exception.Message; exit 1 }"

    if errorlevel 1 (
        echo.
        echo ERROR: Model download failed.
        echo Check your internet connection and Hugging Face URL.
        if exist "%MODEL_FILE%" del "%MODEL_FILE%"
        pause
        exit /b 1
    )

    REM Verify that a file was actually downloaded
    if not exist "%MODEL_FILE%" (
        echo ERROR: Download did not produce a model file.
        pause
        exit /b 1
    )
)

echo Model checkpoint ready.
echo.

REM Create the local virtual environment only if missing
if not exist "%PYTHON%" (
    echo Creating project-local Python environment...

    where py >nul 2>&1
    if not errorlevel 1 (
        py -3.11 -m venv "%VENV_DIR%"
    )

    if not exist "%PYTHON%" (
        python -m venv "%VENV_DIR%"
    )

    if not exist "%PYTHON%" goto setup_error
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
echo Check that Python and requirements.txt are available.
pause
exit /b 1

:server_error
echo.
echo ERROR: The API did not respond within 60 seconds.
echo Check the port, dependencies, and app.py for errors.
pause
exit /b 1
```