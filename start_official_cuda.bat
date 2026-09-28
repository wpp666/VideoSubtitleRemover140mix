@echo off
setlocal
cd /d "%~dp0"
title VSR v1.4.0 CUDA Launcher
echo Starting Video Subtitle Remover (v1.4.0 + CUDA) ...
if not exist python.exe (
  echo Python environment not found.
  echo Please run:  python setup_cuda_env.py
  pause
  exit /b 1
)
python.exe gui.py
if errorlevel 1 (
  echo.
  echo Startup failed. Review the error output above.
  pause
)