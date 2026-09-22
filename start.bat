@echo off
title Akhil Pandey - FastAPI & Uvicorn Server
cls
echo ==============================================================
echo   ⚡ Starting FastAPI Portfolio with Uvicorn...
echo   👉 Portfolio: http://localhost:8000
echo   👉 Admin CMS: http://localhost:8000/admin
echo   👉 API Docs : http://localhost:8000/docs
echo ==============================================================
echo.

python -m uvicorn main:app --reload --port 8000
if %ERRORLEVEL% neq 0 (
    echo.
    echo [!] Trying py -m uvicorn...
    py -m uvicorn main:app --reload --port 8000
)

pause
